import random
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import current_user

from database import mysql

def get_user_tickets_by_month():
    qry = '''
    SELECT
    DATE_FORMAT(`date_created`, '%Y-%m') AS `date`,
    COUNT(*) AS `count`
    FROM tickets
    GROUP BY MONTH(`date_created`)
    ORDER BY date_created ASC;
    '''

def get_permission_level(permission_id):

    #SQL query to get permission level form id, return
    
    permission = 1
    return permission


def add_new_user(email, emp_id, fname, lname, role_id):

    password = emp_id
    userPassword = generate_password_hash(password, method='sha256');

    conn = mysql.connect()
    cursor = conn.cursor()

    default_imgs = ['default1.png', 'default2.png',
                    'default3.png', 'default4.png', 'default5.png']

    imgString = random.choice(default_imgs)

    # TO DO: Verify with IT that all emails are unique...
    qry = '''
    INSERT INTO users (user_id, FK_role_id, fname, lname, email, password, user_img)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    '''

    cursor.execute(qry, (emp_id, role_id, fname, lname, email, userPassword, imgString))
    conn.commit()


    return 

    
def get_user_login_info(email):
    conn = mysql.connect()
    cursor = conn.cursor()

    qry = "SELECT * FROM users WHERE email = %s"
    cursor.execute(qry, (email))
    data = cursor.fetchall()

    ticket_list = []

    columns = [column[0] for column in cursor.description]

    for row in data:
        ticket_list.append(dict(zip(columns, row)))

    return ticket_list


def get_my_watched_tickets():


    conn = mysql.connect()
    cursor = conn.cursor()

    qry = '''
   SELECT * FROM tickets WHERE ticket_id IN 
   (SELECT FK_ticket_id FROM helpdesk.ticket_watching where FK_user_id=%s)
            AND (SELECT COUNT(FK_ticket_id) AS count 
                    FROM helpdesk.ticket_status 
                    WHERE ticket_status.FK_ticket_id=ticket_id
                    AND FK_status_id=(SELECT status_id FROM status_list WHERE status_name = "Closed")) = 0;
   
   '''

    cursor.execute(qry, (current_user.user_id))
    data = cursor.fetchall()

    ticket_list = []

    columns = [column[0] for column in cursor.description]

    for row in data:
        ticket_list.append(dict(zip(columns, row)))

    return ticket_list


def get_my_watched_tickets_updates():

    conn = mysql.connect()
    cursor = conn.cursor()

    qry = '''
            SELECT * FROM ticket_updates 
            WHERE (
                    (FK_ticket_id IN (SELECT FK_ticket_id FROM helpdesk.ticket_watching WHERE FK_user_id=%s)) 
                    OR (FK_ticket_id IN (SELECT ticket_id FROM helpdesk.tickets WHERE created_by=%s))
                ) 
                AND update_date > (SELECT last_login FROM users WHERE user_id=%s) ORDER BY update_date DESC
        '''

    cursor.execute(qry, (current_user.user_id,
                   current_user.user_id, current_user.user_id))
    data = cursor.fetchall()

    ticket_list = []

    columns = [column[0] for column in cursor.description]

    for row in data:
        ticket_list.append(dict(zip(columns, row)))

    return ticket_list


def get_my_assigned_tickets():

    conn = mysql.connect()
    cursor = conn.cursor()

    qry = '''
        SELECT * 
    FROM tickets
    WHERE assigned_to=%s 
    AND (SELECT COUNT(FK_ticket_id) AS count 
        FROM helpdesk.ticket_status 
        WHERE ticket_status.FK_ticket_id=ticket_id 
        AND FK_status_id=(SELECT status_id FROM status_list WHERE status_name = "Closed")) = 0;
   '''

    cursor.execute(qry, (current_user.user_id))
    data = cursor.fetchall()

    ticket_list = []

    columns = [column[0] for column in cursor.description]

    for row in data:
        ticket_list.append(dict(zip(columns, row)))

    return ticket_list

def get_my_permissions():
    conn = mysql.connect()
    cursor = conn.cursor()

    qry = '''
        SELECT permission_level 
    FROM helpdesk.permissions
    WHERE id=%s;
   '''

    cursor.execute(qry, (current_user.FK_role_id))
    data = cursor.fetchall()

    ticket_list = []

    columns = [column[0] for column in cursor.description]

    for row in data:
        ticket_list.append(dict(zip(columns, row)))

    return ticket_list
