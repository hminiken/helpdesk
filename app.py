import os
from flask import Flask
from flask.helpers import url_for
from config import Config

from database import mysql, db, login
from helpdesk.tickets.tickets import tickets_bp
from helpdesk.users.users import users_bp
from helpdesk.dashboard.dashboard import dashboard_bp
from flask_login import LoginManager
from flask_wtf import CsrfProtect

app = Flask(__name__)
app.config.from_object(Config)

app.config['SESSION_COOKIE_SECURE'] = False

db.init_app(app)
login.init_app(app)





app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'jupiter5'
app.config['MYSQL_DATABASE_DB'] = 'helpdesk'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_PORT'] = 3306
mysql.init_app(app)

# Register blueprint
app.register_blueprint(tickets_bp, url_prefix="/tickets")
app.register_blueprint(users_bp, url_prefix="/user")
app.register_blueprint(dashboard_bp, url_prefix="/dashboard")

# #manage sessions


# @app.route('/')
# def index():

#     return "This is the index route"


from flask import Flask, render_template, redirect, flash
from config import Config
from forms import LoginForm




@app.route("/")
def home():
    return redirect(url_for('tickets_bp.show_tickets'))



