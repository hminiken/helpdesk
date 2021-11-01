
from database import mysql
import os


def get_tickets():
    conn = mysql.connect()
    cursor = conn.cursor()

    cursor.execute("SELECT * from tickets ORDER BY ticket_id DESC")
    data = cursor.fetchall()

    ticket_list = []

    columns = [column[0] for column in cursor.description]

    for row in data:
        ticket_list.append(dict(zip(columns, row)))

    return ticket_list


def get_ticket_details(ticket_id):
    conn = mysql.connect()
    cursor = conn.cursor()

    cursor.execute("SELECT * from tickets where ticket_id=" + ticket_id)
    data = cursor.fetchall()

    ticket_list = []

    columns = [column[0] for column in cursor.description]

    for row in data:
        ticket_list.append(dict(zip(columns, row)))

    return ticket_list


def get_ticket_updtes(ticket_id):
    conn = mysql.connect()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * from ticket_updates where FK_ticket_id=" + ticket_id)
    data = cursor.fetchone()

    ticket_list = []

    columns = [column[0] for column in cursor.description]

    for row in data:
        ticket_list.append(dict(zip(columns, row)))

    return ticket_list


def get_user_data():
    conn = mysql.connect()
    cursor = conn.cursor()

    cursor.execute("SELECT * from users ORDER BY fname")
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


def update_assigned_user(uid, ticket_id):

    conn = mysql.connect()
    cursor = conn.cursor()

    update_qry = '''
        UPDATE tickets 
        SET assigned_to = CONCAT(
        (SELECT fname FROM users WHERE user_id = %s),  ' ', 
        (SELECT lname FROM users WHERE user_id = %s))
        WHERE ticket_id = %s
    '''

    cursor.execute(update_qry, (uid, uid, ticket_id))
    conn.commit()

    # Add to status update
    update_qry = '''
        INSERT INTO ticket_updates 
        (update_user, update_description, FK_ticket_id, update_date)
        VALUES (%s,  CONCAT('Assigned to ', 
        (SELECT fname FROM users WHERE user_id = %s),  ' ', 
        (SELECT lname FROM users WHERE user_id = %s), ' by Hillary Miniken')
        , %s,NOW())
    '''

    cursor.execute(update_qry, (uid, uid, uid, ticket_id))
    conn.commit()

    return


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


def insert_ticket_data(details, cust, assy, pn, cat, subcat, priority, created_by):
    conn = mysql.connect()
    cursor = conn.cursor()

    #insert ticket into tickets database
    sql_qry = '''
    INSERT INTO helpdesk.tickets 
    (priority, description, created_by, date_created, assigned_to, 
    customer, assembly, part_number,  category, subcategory) 
    VALUES (%s, %s,  %s, NOW(), %s, %s, %s, %s, %s, %s);
    '''

    # By default tickets are unassigned
    assigned_to = "Unassigned"

    # If checkbox is checked, insert 1 for priority, else 0 
    if priority == 'on':
        priority_bool = 1
    else:
        priority_bool = 0
        
    cursor.execute(sql_qry, (priority_bool, details, created_by, assigned_to,
                    cust, assy, pn, cat, subcat))
    conn.commit()

    # get the id of the request just made and insert filepath
    new_id = cursor.lastrowid
    file_path = "Z:/03. Engineering/Uncontrolled/HelpDeskTickets/" + str(new_id)

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