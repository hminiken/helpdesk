
from database import mysql


def get_tickets():
    conn = mysql.connect()
    cursor = conn.cursor()

    cursor.execute("SELECT * from tickets")
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

    return
