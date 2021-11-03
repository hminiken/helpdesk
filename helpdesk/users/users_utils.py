import random
from werkzeug.security import generate_password_hash, check_password_hash

from database import mysql

def get_user_tickets_by_month():
    qry = '''
    SELECT
    DATE_FORMAT(`date_created`, '%Y-%m') as `date`,
    COUNT(*) as `count`
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

    qry = "SELECT * FROM users where email = %s"
    cursor.execute(qry, (email))
    data = cursor.fetchall()

    ticket_list = []

    columns = [column[0] for column in cursor.description]

    for row in data:
        ticket_list.append(dict(zip(columns, row)))

    return ticket_list
