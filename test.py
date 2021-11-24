import pyodbc
server = '10.1.10.124'
database = 'iERP807'
username = 'engineeringtickets'
password = '{2aVtqkk9jfHLkUus}'   
driver= '{ODBC Driver 17 for SQL Server}'

# with pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1436;DATABASE=iERP807;UID=engineeringtickets;PWD=2aVtqkk9jfHLkUus') as conn:
with pyodbc.connect('Driver={ODBC Driver 17 for SQL Server}; Server=10.1.10.124,1436; Database=iERP807; UID=engineeringtickets;PWD=2aVtqkk9jfHLkUus;') as conn:
# with pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1436;DATABASE='+database+';UID='+username+';PWD='+ password) as conn:
    with conn.cursor() as cursor:
        cursor.execute("SELECT TOP 5 CUS_CustomerID FROM Customer;")
        row = cursor.fetchone()
        while row:
            print (str(row[0]))
            row = cursor.fetchone()