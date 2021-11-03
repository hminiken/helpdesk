from flask import Flask, Blueprint, render_template, request, redirect, url_for
from flask.helpers import flash
from helpdesk.tickets.models import TicketCommentForm,  TicketUpdates
from app import db
from flask_login import current_user
import json

from helpdesk.tickets.ticket_utils import get_ticket_details, get_ticket_updates, get_tickets, get_user_data, get_user_name, insert_ticket_data, update_assigned_user

tickets_bp = Blueprint('tickets_bp', __name__, 
                        template_folder='templates', 
                        static_folder='static')


'''
Show tickets home route. Loads a table of tickets
'''


@tickets_bp.route("/", methods=['GET', 'POST'])
def show_tickets():    
    tickets = get_tickets()
    return render_template('tickets/index.html', tickets=tickets)


'''
Route to display ticket details in side window for clicked table row
'''
@tickets_bp.route('/ticket_details', methods=['GET', 'POST'])
def ticket_details():
    
    ticket_id = request.args.get('ticket_id')
    if ticket_id is None:
        ticket_id = request.form.get('ticket_id')
       
    form = TicketCommentForm()
    if form.validate_on_submit():
        user = TicketUpdates(FK_ticket_id=int(ticket_id), update_user=int(current_user.user_id),
                             update_description=form.comment.data)
        db.session.add(user)
        db.session.commit()
        form.comment.data = ""

    # Get data about specific ticket by id
    details = get_ticket_details(ticket_id)

    # Get a list of users for the assign user drop down
    users = get_user_data()

    # Get the update history for this ticket
    updates = get_ticket_updates(ticket_id)


    return render_template('tickets/ticket_details.html', 
                            details=details,
                            users=users,
                           updates=updates, form=form)


'''
Route to update the assigned user in the database, 
then refresh the display on return
'''
@tickets_bp.route('/assign_user', methods=['GET'])
def user_details():

    # Get User Name from DB to update page
    user_id = request.args.get('user_id')
    ticket_id = request.args.get('ticket_id')

    # Update the assigned user in the database
    update_assigned_user(user_id, ticket_id)

    # Return the ticket id, used to update the ticket details html
    return ticket_id


'''
Route for new ticket form page
'''
@tickets_bp.route("/new_ticket")
def new_ticket():

    # Load the form page
    return render_template('tickets/create_ticket.html')

'''
Route to create the new ticket in the database and reroute home
'''
@tickets_bp.route("/create_ticket", methods=['POST'])
def create_ticket():

    # Get the data input from the form
    cust = request.form.get('cust_input')
    assy = request.form.get('assy_input')
    pn = request.form.get('pn_input')
    cat = request.form.get('cat_select')
    subcat = request.form.get('subcat_select')
    priority = request.form.get('priority_check')
    details = request.form.get('details_input')

    # TO DO: Change to currently logged in user
    created_by = "Hillary Miniken"

    # Insert new ticket into database, create the file path
    insert_ticket_data(details, cust, assy, pn, cat,
                       subcat, priority, created_by)

    return redirect(url_for('tickets_bp.show_tickets'))
