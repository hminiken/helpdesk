from flask_login.login_manager import LoginManager
from flaskext.mysql import MySQL
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
import pyodbc



mysql = MySQL()
db = SQLAlchemy()
login = LoginManager()
mail = Mail()

def conn_database(conn_str):
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()

    return cursor


def conn_erp():

    # erp_conn_str = (
    #     r'Driver=/opt/microsoft/msodbcsql17/lib64/libmsodbcsql-17.8.so.1.1;'
    #     # r'Driver={ODBC Driver 17 for SQL Server};'

    #     r'Server=QEA-ERP805.QEA.local\iERP90,1436;'
    #     r'Database=iERP807;'
    #     r'Trusted_Connection=no;'
    #     r'UID=engineeringtickets;PWD=2aVtqkk9jfHLkUus'
    # )

    erp_conn_str = 'Driver={ODBC Driver 17 for SQL Server}; Server=10.1.10.124,1436; Database=iERP807; UID=engineeringtickets;PWD=2aVtqkk9jfHLkUus;'
    # erp_conn_str = 'Driver=/opt/microsoft/msodbcsql17/lib64/libmsodbcsql-17.8.so.1.1; Server=QEA-ERP805.QEA.local\iERP90,1436; Database=iERP807; UID=engineeringtickets;PWD=2aVtqkk9jfHLkUus;'



    cursorERP = conn_database(erp_conn_str)

    return cursorERP


def conn_unipoint():

    unipoint_conn_str = (
        r'Driver={ODBC Driver 17 for SQL Server};'
        r'Server=QEA-ERP805\ERP805,1436;'
        r'Database=uniPoint_807_Live;'
        r'Trusted_Connection=no;'
        r'UID=support;PWD=lonestar'
    )

    cursorUnipoint = conn_database(unipoint_conn_str)

    return cursorUnipoint
