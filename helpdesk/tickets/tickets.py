'''
* Author: Hillary Miniken
* Email: hminiken@outlook.com
* Date Created: 2021-11-18
* Filename: tickets.py
*
* Description: main script for the tickets blueprint,
               loads the routes for the ticket pages
'''

from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from flask_login.utils import login_required
from globals import TICKET_CLOSED
from helpdesk.tickets.models import NewTicketForm, Subcategory, TicketCommentForm,  TicketUpdates, Tickets
from database import  db
from flask_login import current_user
from helpdesk.tickets.ticket_utils import add_ticket_watcher, close_ticket, create_new_ticket, email_ticket_update, \
                                          get_existing_tickets, get_open_tickets, get_status_options, get_ticket_details, \
                                          get_ticket_status, get_ticket_updates, get_ticket_watchers, get_tickets, \
                                          get_user_data, insert_ticket_data, remove_status, \
                                          remove_ticket_watcher, update_assigned_user, update_ticket_status

tickets_bp = Blueprint('tickets_bp', __name__, 
                        template_folder='templates', 
                        static_folder='static')

@tickets_bp.before_request
def before_request():
    if current_user.is_authenticated == False:
        return redirect(url_for('users_bp.login'))

'''
Show tickets home route. Loads a table of tickets
'''
@tickets_bp.route("/", methods=['GET', 'POST'])
def show_tickets():    
    tickets = get_tickets()
    open_count = get_open_tickets()

    return render_template('tickets/index.html', tickets=tickets,
                           open_count=open_count)


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

        # Send the emails:
        update_msg = current_user.fname + " " + \
            current_user.lname + " has added a new comment: \n\n     " + form.comment.data

        form.comment.data = ""

        email_ticket_update(ticket_id, update_msg)

    # Get data about specific ticket by id
    details = get_ticket_details(ticket_id)

    # Get a list of users for the assign user drop down
    users = get_user_data()

    # Get the update history for this ticket
    updates = get_ticket_updates(ticket_id)
    status_options = get_status_options()
    ticket_status = get_ticket_status(ticket_id)
    ticket_watchers = get_ticket_watchers(ticket_id)

    new_ticket_form = NewTicketForm()


    return render_template('tickets/ticket_details.html', 
                            details=details,
                            users=users,
                           new_ticket_form=new_ticket_form,
                           updates=updates, form=form, 
                           status_options=status_options,
                           ticket_status=ticket_status,
                           ticket_watchers=ticket_watchers)


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
Route to add a watcher to the ticket in the database, 
then refresh the display on return
'''
@tickets_bp.route('/assign_watcher', methods=['GET'])
def assign_watcher():

    # Get User Name from DB to update page
    user_id = request.args.get('user_id')
    ticket_id = request.args.get('ticket_id')

    ticket_watchers = get_ticket_watchers(ticket_id)

    watcher_exists = False
    for item in ticket_watchers:
        if item['user_id'] == int(user_id):
            watcher_exists = True

    if watcher_exists == False:
        # Only update db if status doesn't already exist
        add_ticket_watcher(user_id, ticket_id)        
    else:
        #remove that status
        remove_ticket_watcher(user_id, ticket_id)

    # Return the ticket id, used to update the ticket details html
    return ticket_id


'''
Route to update the assigned user in the database, 
then refresh the display on return
'''
@tickets_bp.route('/assign_status', methods=['GET'])
def assign_statu():

    # Get User Name from DB to update page
    status_id = request.args.get('status_id')
    ticket_id = request.args.get('ticket_id')
    status_name = ""
    status = get_ticket_status(ticket_id)
    
    status_exists = False
    update_msg = ""
    for item in status:
        if item['status_id'] == int(status_id):
            status_exists = True

    if status_exists == False:
        # Only update db if status doesn't already exist
        update_ticket_status(status_id, ticket_id)
        if int(status_id) == TICKET_CLOSED:
            #close ticket
            close_ticket(ticket_id)
        status = get_ticket_status(ticket_id)
        status_name = status[0]['status_name']
        update_msg = current_user.fname + " " + current_user.lname + \
            " has updated the status to: " + status_name
    else:
        #remove that status
        remove_status(status_id, ticket_id)
        update_msg = current_user.fname + " " + current_user.lname + \
            " has removed the status: " + status_name

    # Send the emails:
    email_ticket_update(ticket_id, update_msg)

    # Return the ticket id, used to update the ticket details html
    return ticket_id



'''
Route for new ticket form page
'''
@tickets_bp.route("/new_ticket", methods=['GET','POST'])
def new_ticket():

    #instantiate the form, and get the initial choices for the subcategory, where category is 1
    form = NewTicketForm()
    form.subcat.choices = [(int(subcategory.id), subcategory.subcategory_name)
                           for subcategory in Subcategory.query.filter_by(FK_category_id='1').all()]

    if request.method == 'POST' and form.validate_on_submit():
        create_new_ticket(form)
        return redirect(url_for('tickets_bp.show_tickets'))


    return render_template('tickets/create_ticket.html', form=form)


'''
'''
@tickets_bp.route("/new_ticket/<category>", methods=['GET', 'POST'])
def new_ticket_subcatgory(category):

    subcats = Subcategory.query.filter_by(FK_category_id=category).all()

    subcatsList = []

    for subcat in subcats:
        subcatObj = {}
        subcatObj['id'] = int(subcat.id)
        subcatObj['subcategory_name'] = subcat.subcategory_name
        subcatsList.append(subcatObj)


    return jsonify({'subcats' : subcatsList})


'''
Route to create the new ticket in the database and reroute home
'''
@tickets_bp.route("/create_ticket", methods=['GET', 'POST'])
def create_ticket():

    # Get the data input from the form
    cust = request.form.get('cust_input')
    assy = request.form.get('assy_input')
    pn = request.form.get('pn_input')
    wo = request.form.get('wo_input')
    cat = request.form.get('cat_select')
    subcat = request.form.get('subcat_select')
    priority = request.form.get('priority_check')
    details = request.form.get('details_input')

    # Insert new ticket into database, create the file path
    insert_ticket_data(details, cust, assy, pn, cat,
                       subcat, priority, wo)

    return redirect(url_for('tickets_bp.show_tickets'))


'''
Route for ticket creation page, fetch all the open tickets
for that customer, then display on the right hand possible
'''
@tickets_bp.route('/already_created', methods=['GET', 'POST'])
def created_ticket_list():

    cust = request.args.get('cust')
    
    # Get data about specific ticket by id
    ticket_list = get_existing_tickets(cust)

    return render_template('tickets/create.html',
                           ticket_list=ticket_list)


@tickets_bp.route("/edit_ticket", methods=['GET', 'POST'])
def edit_ticket():

    #instantiate the form, and get the initial choices for the subcategory, where category is 1
    form = NewTicketForm()

    ticket_id = request.args.get('ticket_id')
    ticket_data = Tickets.query.filter_by(ticket_id=ticket_id).first()

 
    if request.method == 'GET':
        form.assembly.data = ticket_data.assembly
        form.priority.data = ticket_data.priority
        form.workorder.data = ticket_data.work_order
        form.description.data = ticket_data.description
        form.partnumber.data = ticket_data.part_number
        form.customer.data = ticket_data.customer
        form.category.data = ticket_data.category
        form.subcat.data = ticket_data.subcategory

   
        form.subcat.choices = [(int(subcategory.id), subcategory.subcategory_name)
                           for subcategory in Subcategory.query.filter_by(FK_category_id='1').all()]

    if request.method == 'POST' and form.validate_on_submit():
        ticket_data.assembly = form.assembly.data 
        ticket_data.priority = form.priority.data 
        ticket_data.work_order = form.workorder.data 
        ticket_data.description = form.description.data 
        ticket_data.part_number = form.partnumber.data 
        ticket_data.customer = form.customer.data 
        ticket_data.category = form.category.data 
        ticket_data.subcategory = form.subcat.data 

        db.session.commit()
        return redirect(url_for('tickets_bp.show_tickets'))


    return render_template('tickets/create_ticket.html', form=form)
