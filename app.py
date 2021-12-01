from flask import Flask
from flask.helpers import url_for
from config import Config

from database import mail, db
from database import mysql, db, login, mail, csrf
from helpdesk.tickets.tickets import tickets_bp
from helpdesk.users.users import users_bp
from helpdesk.dashboard.dashboard import dashboard_bp
from flask import Flask


app = Flask(__name__)
app.config.from_object(Config)

app.config['SESSION_COOKIE_SECURE'] = False

app.app_context().push()

db.init_app(app)

with app.app_context():
    db.create_all()
    
login.init_app(app)

mail.init_app(app)


app.config['MYSQL_DATABASE_USER'] = 'localadmin'
app.config['MYSQL_DATABASE_PASSWORD'] = 'um8%JKid#G6N8ep2'
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



# Home route, redirects to ticket list
@app.route("/")
def home():
    return redirect(url_for('tickets_bp.show_tickets'))


if __name__ == "__main__":
    app.run(port=5050)




