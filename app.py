import os
from flask import Flask
from flask.helpers import url_for
from config import Config

from database import mysql, db, login, mail
from helpdesk.users.users import users_bp
from flask import Flask
from helpdesk.users.users import users_bp
from helpdesk.dashboard.dashboard import dashboard_bp
from helpdesk.tickets.tickets import tickets_bp

app = Flask(__name__)
app.config.from_object(Config)

app.config['SESSION_COOKIE_SECURE'] = False

app.app_context().push()
db.init_app(app)

with app.app_context():
    db.create_all()
    
login.init_app(app)

mail.init_app(app)



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


from flask import Flask, render_template, redirect, flash
from config import Config
from forms import LoginForm




@app.route("/")
def home():
    return redirect(url_for('tickets_bp.show_tickets'))


if __name__ == "__main__":
    app.run(host='0.0.0.0')
