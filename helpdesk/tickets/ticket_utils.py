'''
* Author: Hillary Miniken
* Email: hminiken@outlook.com
* Date Created: 2021-11-18
* Filename: ticket_utils.py
*
* Description: Functions for use in the tickets.py script. 
               Fetches and processes data from database to
               be loaded onto the ticket pages.
'''

from datetime import datetime
from flask.templating import render_template
from flask_mail import Message
from pymysql import NULL
from database import mysql
import os
from database import db, mail
from flask_login import current_user
from globals import TICKET_CLOSED
from helpdesk.tickets.models import Subcategory, Tickets

#  -----------------------------------------------------------
# 
#  ======= Section to load all the tickets on the page =======
#
#  -----------------------------------------------------------

def get_tickets():
    conn = mysql.connect()
    cursor = conn.cursor()

    qry = '''SELECT *, 
    (SELECT CONCAT(fname, ' ', lname) FROM users WHERE user_id=created_by ) AS created, 
    (SELECT CONCAT(fname, ' ', lname) FROM users WHERE user_id=assigned_to ) AS assigned  ,
    (SELECT 
	(SELECT status_name FROM status_list WHERE status_id = FK_status_id) as status_name 
	FROM ticket_status 
	WHERE FK_ticket_id=ticket_id ORDER BY FK_status_id ASC LIMIT 1) as ticket_status,
    (SELECT 
	(SELECT status_badge FROM status_list WHERE status_id = FK_status_id) as status_name 
	FROM ticket_status 
	WHERE FK_ticket_id=ticket_id ORDER BY FK_status_id ASC LIMIT 1) as ticket_badge
    FROM tickets 
    ORDER BY ticket_id DESC

    '''

    # WHERE closed_by IS NULL

    cursor.execute(qry)
    data = cursor.fetchall()

    ticket_list = []

    columns = [column[0] for column in cursor.description]

    for row in data:
        ticket_list.append(dict(zip(columns, row)))

    return ticket_list


def get_closed_tickets():
    conn = mysql.connect()
    cursor = conn.cursor()

    qry = '''SELECT *, 
    (SELECT CONCAT(fname, ' ', lname) FROM users WHERE user_id=created_by ) AS created, 
    (SELECT CONCAT(fname, ' ', lname) FROM users WHERE user_id=assigned_to ) AS assigned  
    FROM tickets 
    WHERE closed_by IS NOT NULL
    ORDER BY ticket_id DESC

    '''
    cursor.execute(qry)
    data = cursor.fetchall()

    ticket_list = []

    columns = [column[0] for column in cursor.description]

    for row in data:
        ticket_list.append(dict(zip(columns, row)))

    return ticket_list


def get_open_tickets():
    conn = mysql.connect()
    cursor = conn.cursor()

    qry = '''SELECT COUNT(ticket_id) as count
    from tickets 
    WHERE closed_by IS NOT NULL
    ORDER BY ticket_id DESC

    '''
    cursor.execute(qry)
    data = cursor.fetchall()

    ticket_list = []

    columns = [column[0] for column in cursor.description]

    for row in data:
        ticket_list.append(dict(zip(columns, row)))

    return ticket_list


#  -----------------------------------------------------------
#
#  =======       Section to load ticket details       =======
#
#  -----------------------------------------------------------


def get_ticket_details(ticket_id):
    conn = mysql.connect()
    cursor = conn.cursor()

    qry = '''
        SELECT *, 
        (SELECT CONCAT(fname, ' ', lname) FROM users WHERE user_id=created_by ) AS created, 
        (SELECT CONCAT(fname, ' ', lname) FROM users WHERE user_id=assigned_to ) AS assigned, 
        (SELECT user_img FROM users WHERE user_id=assigned_to ) AS user_assigned_img, 
        (SELECT user_img FROM users WHERE user_id=created_by ) AS user_created_img, 
        (SELECT CONCAT(fname, ' ', lname) FROM users WHERE user_id=closed_by ) AS closed 
        FROM tickets WHERE ticket_id=%s;
    '''

    cursor.execute(qry, (ticket_id))
    data = cursor.fetchall()

    ticket_list = []

    columns = [column[0] for column in cursor.description]

    for row in data:
        ticket_list.append(dict(zip(columns, row)))

    return ticket_list


def get_ticket_updates(ticket_id):
    conn = mysql.connect()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * ROM ticket_updates WHERE FK_ticket_id=" + ticket_id)
    data = cursor.fetchone()

    ticket_list = []

    columns = [column[0] for column in cursor.description]

    for row in data:
        ticket_list.append(dict(zip(columns, row)))

    return ticket_list


def get_ticket_status(ticket_id):
    conn = mysql.connect()
    cursor = conn.cursor()

    sql = '''
    SELECT 
    (SELECT status_id FROM status_list WHERE status_id = FK_status_id) as status_id, 
    (SELECT status_badge FROM status_list WHERE status_id = FK_status_id) as status_badge, 
    (SELECT status_name FROM status_list WHERE status_id = FK_status_id) as status_name 
    FROM ticket_status 
    WHERE FK_ticket_id = %s;
    '''

    cursor.execute(sql, (ticket_id))
    data = cursor.fetchall()

    user_list = []

    columns = [column[0] for column in cursor.description]

    for row in data:
        user_list.append(dict(zip(columns, row)))

    return user_list


def get_user_data():
    conn = mysql.connect()
    cursor = conn.cursor()

    qry = '''
    SELECT *, 	(SELECT permission_department FROM permissions WHERE id=FK_role_id) as department FROM users ORDER BY fname
    '''

    cursor.execute(qry)
    data = cursor.fetchall()

    user_list = []

    columns = [column[0] for column in cursor.description]

    for row in data:
        user_list.append(dict(zip(columns, row)))

    return user_list


def get_status_options():

    conn = mysql.connect()
    cursor = conn.cursor()

    sql = '''
    SELECT status_id, status_name, status_badge FROM status_list;
    '''

    cursor.execute(sql)
    data = cursor.fetchall()

    user_list = []

    columns = [column[0] for column in cursor.description]

    for row in data:
        user_list.append(dict(zip(columns, row)))

    return user_list


def get_user_name(uid):
    conn = mysql.connect()
    cursor = conn.cursor()

    cursor.execute("SELECT users.fname, users.lname FROM users WHERE user_id =" + uid)
    data = cursor.fetchall()

    user_list = []

    columns = [column[0] for column in cursor.description]

    for row in data:
        user_list.append(dict(zip(columns, row)))

    return user_list


def get_ticket_updates(ticket_id):

    conn = mysql.connect()
    cursor = conn.cursor()

    sql_qry = '''SELECT update_description, update_date, CONCAT(users.fname, ' ' , users.lname) as user
                FROM helpdesk.ticket_updates 
                JOIN users ON users.user_id = ticket_updates.update_user 
                WHERE FK_ticket_id = %s ORDER BY update_date DESC;'''

    cursor.execute(sql_qry, (ticket_id))
    data = cursor.fetchall()

    update_list = []

    columns = [column[0] for column in cursor.description]

    for row in data:
        update_list.append(dict(zip(columns, row)))

    return update_list


#  -----------------------------------------------------------
#
#  =======         Section to update a ticket         =======
#
#  -----------------------------------------------------------


def update_assigned_user(uid, ticket_id):

    conn = mysql.connect()
    cursor = conn.cursor()

    update_qry = '''
        UPDATE tickets 
        SET assigned_to = %s
        WHERE ticket_id = %s
    '''

    cursor.execute(update_qry, (uid, int(ticket_id)))
    conn.commit()

    # Add to status update
    update_qry = '''
        INSERT INTO ticket_updates 
        (update_user, update_description, FK_ticket_id, update_date)
        VALUES (%s,  CONCAT('Assigned to ', 
        (SELECT fname FROM users WHERE user_id = %s),  ' ', 
        (SELECT lname FROM users WHERE user_id = %s), ' by ',
        
        CONCAT( (SELECT fname FROM users WHERE user_id = %s),  ' ', 
        (SELECT lname FROM users WHERE user_id = %s)))        
        , %s, NOW())
    '''

    cursor.execute(update_qry, (current_user.user_id, uid,
                   uid,  current_user.user_id,  current_user.user_id, int(ticket_id)))
    conn.commit()

    # Remove status "unassigned if exists"
    update_qry = '''
        DELETE FROM helpdesk.ticket_status 
        WHERE FK_ticket_id=%s AND FK_status_id=%s;
    '''

    cursor.execute(update_qry, (int(ticket_id), 4))
    conn.commit()

    return


def update_ticket_status(status_id, ticket_id):

    conn = mysql.connect()
    cursor = conn.cursor()

    uid = current_user.id

    update_desc = current_user.fname + " " + current_user.lname + " set the status to "

       # Add to status update
    update_qry = '''
        INSERT INTO ticket_updates 
        (update_user, update_description, FK_ticket_id, update_date)
        VALUES (%s, CONCAT(%s, 
        (SELECT status_name FROM status_list WHERE status_id = %s)),
        %s, NOW())
        '''

    cursor.execute(update_qry, (current_user.user_id, update_desc, status_id, ticket_id))
    conn.commit()


    # add new status to the top
    update_qry = '''
        INSERT INTO ticket_status 
        (FK_ticket_id, FK_status_id) 
        VALUES (%s, %s);
    '''

    cursor.execute(update_qry, (ticket_id, status_id))
    conn.commit()


    return


def remove_status(status_id, ticket_id):
    conn = mysql.connect()
    cursor = conn.cursor()

    update_qry = '''
        DELETE FROM ticket_status 
        WHERE FK_ticket_id = %s AND  FK_status_id = %s
    '''

    cursor.execute(update_qry, (ticket_id, status_id))
    conn.commit()

    update_desc = current_user.fname + " " + \
        current_user.lname + " removed the status "

    # Add to status update
    update_qry = '''
        INSERT INTO ticket_updates 
        (update_user, update_description, FK_ticket_id, update_date)
        VALUES (%s, CONCAT(%s, 
        (SELECT status_name FROM status_list WHERE status_id = %s)),
        %s, NOW())
        '''

    cursor.execute(update_qry, (current_user.user_id,
                   update_desc, status_id, ticket_id))
    conn.commit()

    if int(status_id) == TICKET_CLOSED:
        update_qry = '''
        UPDATE tickets
        SET closed_by=NULL, date_closed=NULL
        WHERE ticket_id=%s
        '''

        cursor.execute(update_qry, (ticket_id))
        conn.commit()


    return


def close_ticket(ticket_id):
    conn = mysql.connect()
    cursor = conn.cursor()

    update_qry = '''
        UPDATE tickets 
        SET closed_by = %s, date_closed = NOW()
        WHERE ticket_id = %s
    '''

    cursor.execute(update_qry, (current_user.user_id, int(ticket_id)))
    conn.commit()


def email_ticket_update(ticket_id, update_msg):
    conn = mysql.connect()
    cursor = conn.cursor()

    sql_qry = '''
                SELECT FK_user_id as user_id,
                (SELECT CONCAT(fname, ' ', lname) FROM users WHERE user_id=FK_user_id) AS watcher,          
                (SELECT ticket_watched_updates FROM users WHERE user_id=FK_user_id) AS send_update,
                (SELECT email FROM users WHERE user_id=FK_user_id) AS email
                FROM helpdesk.ticket_watching
                WHERE FK_ticket_id=%s;
                '''

    cursor.execute(sql_qry, (ticket_id))
    data = cursor.fetchall()

    watcher_emails = []

    columns = [column[0] for column in cursor.description]

    for row in data:
        watcher_emails.append(dict(zip(columns, row)))

    # Get the creator
    sql_qry = '''
            SELECT 
            (SELECT CONCAT(fname, ' ', lname) FROM users WHERE user_id=created_by ) AS created, 
            (SELECT ticket_created_updates FROM users WHERE user_id=created_by ) AS send_update,
            (SELECT email FROM users WHERE user_id=created_by) AS email    
            FROM tickets WHERE ticket_id=%s;
                '''

    cursor.execute(sql_qry, (ticket_id))
    data = cursor.fetchall()

    created_email = []

    columns = [column[0] for column in cursor.description]

    for row in data:
        created_email.append(dict(zip(columns, row)))

    # Get the assignee
    sql_qry = '''
                SELECT  
                (SELECT CONCAT(fname, ' ', lname) FROM users WHERE user_id=assigned_to ) AS created, 
                (SELECT ticket_assigned_updates FROM users WHERE user_id=assigned_to ) AS send_update,
                (SELECT email FROM users WHERE user_id=assigned_to ) AS email       
                FROM tickets  WHERE ticket_id=%s
                '''

    cursor.execute(sql_qry, (ticket_id))
    data = cursor.fetchall()

    assigned_email = []

    columns = [column[0] for column in cursor.description]

    for row in data:
        assigned_email.append(dict(zip(columns, row)))


    # Now create the email list
    email_msg = create_email(ticket_id, update_msg)


    for item in watcher_emails:
        if item['send_update'] == 1:
            email_msg.add_recipient(item['email'])

    for item in assigned_email:
        if item['send_update'] == 1:
            email_msg.add_recipient(item['email'])
    
    for item in created_email:
        if item['send_update'] == 1:
            email_msg.add_recipient(item['email'])

    if len(email_msg.recipients) > 0:
        mail.send(email_msg)

    return

def create_email(t_id, update_msg):

    ticket = Tickets.query.filter_by(ticket_id=t_id).first()

    subject = "[Engineering Ticket #" + str(t_id) + "] " + ticket.category + " - " + ticket.subcategory
    
    email_msg = Message(
        subject=subject,
        sender="engineeringtickets@qualitel.net",
    )

    email_msg.html = render_template(
        'tickets/ticket_update_email.html', description=ticket.description, update_message=update_msg, 
        ticket_num=t_id, assembly=ticket.assembly, category=ticket.category, subcategory=ticket.subcategory,
        workorder=ticket.work_order, partnumber=ticket.part_number)

    return email_msg


#  -----------------------------------------------------------
#
#  =======         Section for Ticket Watching         =======
#
#  -----------------------------------------------------------

def get_ticket_watchers(ticket_id):

    conn = mysql.connect()
    cursor = conn.cursor()

    sql_qry = '''
            SELECT FK_user_id as user_id,
            (SELECT CONCAT(fname, ' ', lname) FROM users WHERE user_id=FK_user_id) AS watcher,
            (SELECT user_img FROM users WHERE user_id=FK_user_id) AS user_img,
            (SELECT 
                (SELECT permission_department FROM permissions WHERE id=FK_role_id) 
                FROM helpdesk.users WHERE user_id=FK_user_id) AS department
            FROM helpdesk.ticket_watching
            WHERE FK_ticket_id=%s;
                        '''

    cursor.execute(sql_qry, (ticket_id))
    data = cursor.fetchall()

    update_list = []

    columns = [column[0] for column in cursor.description]

    for row in data:
        update_list.append(dict(zip(columns, row)))

    return update_list


def add_ticket_watcher(user_id, ticket_id):
    conn = mysql.connect()
    cursor = conn.cursor()

    # Add to status update
    update_qry = '''
        INSERT INTO ticket_watching 
        (FK_ticket_id, FK_user_id)
        VALUES (%s, %s)
        '''

    cursor.execute(update_qry, (ticket_id, user_id))
    conn.commit()

    return


def remove_ticket_watcher(user_id, ticket_id):
    conn = mysql.connect()
    cursor = conn.cursor()

    # Add to status update
    update_qry = '''
        DELETE FROM ticket_watching 
        WHERE FK_ticket_id = %s AND FK_user_id = %s
        '''

    cursor.execute(update_qry, (ticket_id, user_id))
    conn.commit()

    return


#  -----------------------------------------------------------
#
#  =======           Section for New Tickets           =======
#
#  -----------------------------------------------------------


def get_existing_tickets(cust):

    conn = mysql.connect()
    cursor = conn.cursor()

    sql_qry = '''
            SELECT *
            FROM tickets
            WHERE customer LIKE %s;
            '''

    cursor.execute(sql_qry, (cust + "%"))
    data = cursor.fetchall()

    update_list = []

    columns = [column[0] for column in cursor.description]

    for row in data:
        update_list.append(dict(zip(columns, row)))

    return update_list


def insert_ticket_data(details, cust, assy, pn, cat, subcat, priority, wo):
    conn = mysql.connect()
    cursor = conn.cursor()

    #insert ticket into tickets database
    sql_qry = '''
    INSERT INTO helpdesk.tickets 
    (priority, description, created_by, date_created, assigned_to, 
    customer, assembly, part_number, work_order, category, subcategory) 
    VALUES (%s, %s,  %s, NOW(), %s, %s, %s, %s, %s, %s, %s);
    '''

    # By default tickets are unassigned
    assigned_to = None
    created_by = current_user.user_id

    # If checkbox is checked, insert 1 for priority, else 0
    if priority == 'on':
        priority_bool = 1
    else:
        priority_bool = 0

    cursor.execute(sql_qry, (priority_bool, details, created_by, assigned_to,
                             cust, assy, pn, wo, cat, subcat))
    conn.commit()
    new_id = cursor.lastrowid

    #Add status of unassigned
    sql_qry = '''
    INSERT INTO ticket_status
    (FK_ticket_id, FK_status_id)
    VALUES(%s, %s)
       '''

    cursor.execute(sql_qry, (4, new_id))
    conn.commit()

    # get the id of the request just made and insert filepath
    
    file_path = "Z:/03. Engineering/Uncontrolled/HelpDeskTickets/" + \
        str(new_id)

    sql_qry = '''
    UPDATE helpdesk.tickets 
    SET attachments =  %s
    WHERE
    ticket_id = %s   '''

    cursor.execute(sql_qry, (file_path, new_id))
    conn.commit()

    # Make the path in QMS and open
    os.mkdir(file_path)
    os.startfile(file_path)

    return


def create_new_ticket(form):
    attachments = "Z:/03. Engineering/Uncontrolled/HelpDeskTickets/"
    date = datetime.now()
    created = current_user.user_id
    subcat_name = Subcategory.query.filter_by(id=form.subcat.data).first()

    # Create the Tickets object to insert into the database
    ticket = Tickets(priority=form.priority.data, description=form.description.data,
                     customer=form.customer.data, assembly=form.assembly.data, part_number=form.partnumber.data,
                     work_order=form.workorder.data, category=form.category.data.category_name, subcategory=subcat_name.subcategory_name,
                     attachments=attachments, date_created=date, created_by=created)

    # Add to the database                     
    db.session.add(ticket)
    db.session.commit()

    # Get the id so we can update the attachments field
    ticket_id = ticket.id
    ticket_created = Tickets.query.get(ticket_id)
    file_path = attachments + str(ticket_id)
    ticket_created.attachments = file_path
    db.session.commit()


    #make the folder and open
    # Make the path in QMS and open
    os.mkdir(file_path)
    os.startfile(file_path)
   
    return

