from flask_login.login_manager import LoginManager
from flaskext.mysql import MySQL
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
import pyodbc
from flask_wtf.csrf import CSRFProtect


mysql = MySQL()
db = SQLAlchemy()
login = LoginManager()
mail = Mail()
csrf = CSRFProtect()

def conn_database(conn_str):
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()

    return cursor


def conn_erp():

    # TO DO: Update so password isn't hardcoded
    erp_conn_str = (r'Driver={ODBC Driver 17 for SQL Server}; '
                    r'Server=10.1.10.124,1436; '
                    r'Database=iERP807; '
                    r'UID=engineeringtickets;'
                    r'PWD=2aVtqkk9jfHLkUus;'
                    )

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
