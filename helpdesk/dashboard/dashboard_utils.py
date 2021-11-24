from database import mysql


def get_dashboard_tickets():
    conn = mysql.connect()
    cursor = conn.cursor()

    qry = '''SELECT  
     IFNULL((Select CONCAT(fname, ' ', lname) from users where user_id=created_by ), "NONE") AS created, 
     IFNULL((Select CONCAT(fname, ' ', lname) from users where user_id=assigned_to ), "NONE") AS assigned,
     IFNULL((Select CONCAT(fname, ' ', lname) from users where user_id=closed_by ), "NONE") AS closed  
    from tickets ORDER BY ticket_id DESC
    '''
    cursor.execute(qry)
    data = cursor.fetchall()

    ticket_list = []

    columns = [column[0] for column in cursor.description]

    for row in data:
        ticket_list.append(dict(zip(columns, row)))

    return ticket_list


def get_dashboard_tickets_by_category():
    conn = mysql.connect()
    cursor = conn.cursor()

    qry = '''SELECT category, COUNT(*) as count
        FROM tickets    
        Where closed_by IS NULL  
        GROUP BY category;
    '''
    cursor.execute(qry)
    data = cursor.fetchall()

    ticket_list = []

    columns = [column[0] for column in cursor.description]

    for row in data:
        ticket_list.append(dict(zip(columns, row)))

    return ticket_list


def get_dashboard_tickets_by_subcategory():
    conn = mysql.connect()
    cursor = conn.cursor()

    qry = '''SELECT subcategory, COUNT(*) as count
        FROM tickets    
        Where closed_by IS NULL  
        GROUP BY subcategory;
    '''
    cursor.execute(qry)
    data = cursor.fetchall()

    ticket_list = []

    columns = [column[0] for column in cursor.description]

    for row in data:
        ticket_list.append(dict(zip(columns, row)))

    return ticket_list


def get_dashboard_tickets_by_assigned():
    conn = mysql.connect()
    cursor = conn.cursor()

    qry = '''SELECT 
    IFNULL((Select CONCAT(fname, ' ', lname) from users where user_id=assigned_to ),"NONE") AS assigned, COUNT(*)  as count
    FROM tickets  
    Where closed_by IS NULL    
    GROUP BY assigned_to;
    '''
    cursor.execute(qry)
    data = cursor.fetchall()

    ticket_list = []

    columns = [column[0] for column in cursor.description]

    for row in data:
        ticket_list.append(dict(zip(columns, row)))

    return ticket_list


def get_dashboard_tickets_by_created():
    conn = mysql.connect()
    cursor = conn.cursor()

    qry = '''SELECT 
    IFNULL((Select CONCAT(fname, ' ', lname) from users where user_id=created_by ),"NONE") AS created, COUNT(*) as count
    FROM tickets      
    Where closed_by IS NULL
    GROUP BY created_by;
    '''
    cursor.execute(qry)
    data = cursor.fetchall()

    ticket_list = []

    columns = [column[0] for column in cursor.description]

    for row in data:
        ticket_list.append(dict(zip(columns, row)))

    return ticket_list


   



def get_dashboard_tickets_by_closed():
    conn = mysql.connect()
    cursor = conn.cursor()

    qry = '''SELECT 
    IFNULL((Select CONCAT(fname, ' ', lname) from users where user_id=closed_by ),"NONE") AS closed, COUNT(*) as count
    FROM tickets   
    Where closed_by IS NOT NULL   
    GROUP BY closed_by;
    '''
    cursor.execute(qry)
    data = cursor.fetchall()

    ticket_list = []

    columns = [column[0] for column in cursor.description]

    for row in data:
        ticket_list.append(dict(zip(columns, row)))

    return ticket_list


def get_dashboard_total():
    conn = mysql.connect()
    cursor = conn.cursor()

    qry = '''SELECT 
    count(*)  as count
    FROM tickets      
    Where closed_by IS NULL;
    '''
    cursor.execute(qry)
    data = cursor.fetchall()

    ticket_list = []

    columns = [column[0] for column in cursor.description]

    for row in data:
        ticket_list.append(dict(zip(columns, row)))

    return ticket_list


def get_closed_last_x_days():
    conn = mysql.connect()
    cursor = conn.cursor()

    qry = '''SELECT 
    count(*)  as count
    FROM tickets      
    Where closed_by IS NOT NULL and date_closed BETWEEN CURDATE() - INTERVAL 5 DAY AND CURDATE()
    
    '''
    cursor.execute(qry)
    data = cursor.fetchall()

    ticket_list = []

    columns = [column[0] for column in cursor.description]

    for row in data:
        ticket_list.append(dict(zip(columns, row)))

    return ticket_list


def get_opened_last_x_days():
    conn = mysql.connect()
    cursor = conn.cursor()

    qry = '''SELECT 
    count(*) as count
    FROM tickets      
    Where date_created BETWEEN CURDATE() - INTERVAL 5 DAY AND CURDATE();
    
    '''
    cursor.execute(qry)
    data = cursor.fetchall()

    ticket_list = []

    columns = [column[0] for column in cursor.description]

    for row in data:
        ticket_list.append(dict(zip(columns, row)))

    return ticket_list
