from flask import Flask

from database import mysql
from helpdesk.tickets.tickets import tickets_bp

app = Flask(__name__)

app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'jupiter5'
app.config['MYSQL_DATABASE_DB'] = 'helpdesk'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_PORT'] = 3306
mysql.init_app(app)

# Register blueprint
app.register_blueprint(tickets_bp, url_prefix="/tickets")

@app.route('/')
def index():

    return "This is the index route"



