from flask import Blueprint, render_template, request

from helpdesk.tickets.ticket_utils import get_ticket_details, get_ticket_updates, get_tickets, get_user_data, get_user_name, update_assigned_user

tickets_bp = Blueprint('tickets_bp', __name__, 
                        template_folder='templates', 
                        static_folder='static')
                        # static_url_path='assets')



@tickets_bp.route("/")
def list():
    
    tickets = get_tickets()
    return render_template('tickets/index.html', tickets=tickets)


@tickets_bp.route('/ticket_details', methods=['GET'])
def npi_tasks():
    ticket_id = request.args.get('ticket_id')
    details = get_ticket_details(ticket_id)
    users = get_user_data()
    updates = get_ticket_updates(ticket_id)

    return render_template('tickets/ticket_details.html', 
                            details=details,
                            users=users,
                           updates=updates)


@tickets_bp.route('/assign_user', methods=['GET'])
def user_details():

    # Get User Name from DB to update page
    user_id = request.args.get('user_id')
    ticket_id = request.args.get('ticket_id')

    update_assigned_user(user_id, ticket_id)

    # user_id = get_user_name(user_id)
    # userName = user_id[0]['fname'] + " " + user_id[0]['lname']

    # Update database with the current assignee

    # Insert into update history

    # return user name
    return ticket_id


@tickets_bp.route("/new_ticket")
def new_ticket():

    tickets = get_tickets()
    return render_template('tickets/create_ticket.html', tickets=tickets)
