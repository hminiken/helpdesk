from flask_login.login_manager import LoginManager
from flaskext.mysql import MySQL
from flask_sqlalchemy import SQLAlchemy



mysql = MySQL()
db = SQLAlchemy()
login = LoginManager()
