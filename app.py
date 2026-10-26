import os
from flask import Flask
from flask.helpers import url_for
from config import Config

from database import mail, db
from database import mysql, db, login, mail, csrf
from helpdesk.tickets.tickets import tickets_bp
from helpdesk.users.users import users_bp
from helpdesk.dashboard.dashboard import dashboard_bp


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
app.config['MYSQL_DATABASE_PASSWORD'] = os.environ.get('MYSQL_DATABASE_PASSWORD')
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





# import flask
# from flask import request, jsonify

# app = flask.Flask(__name__)
# app.config["DEBUG"] = True

# # Create some test data for our catalog in the form of a list of dictionaries.
# data_science_books = [
#     {'id': 0,
#      'title': 'Data Science (MIT Press Essential Knowledge series)',
#      'authors': 'John D Kelleher and Brendan Tierney',
#      'price': '£9.45',
#      'published': '6 Apr 2018',
#      'url': 'https://www.amazon.co.uk/Data-Science-Press-Essential-Knowledge/dp/0262535432/ref=sr_1_3?keywords=data+science&qid=1636616265&sr=8-3'},
#     {'id': 0,
#      'title': 'Data Science For Dummies, 2nd Edition (For Dummies (Computer/Tech))',
#      'authors': 'Lillian Pierson',
#      'price': '15.65',
#      'published': '24 Feb 2017',
#      'url': 'https://www.amazon.co.uk/Data-Science-Dummies-2nd-Computers/dp/1119327636/ref=sr_1_4?keywords=data+science&qid=1636616265&sr=8-4'},
#     {'id': 0,
#      'title': 'Data Science from Scratch: First Principles with Python',
#      'authors': 'Joel Grus',
#      'price': '£29.99',
#      'published': '30 Apr 2019',
#      'url': 'https://www.amazon.co.uk/Data-Science-Scratch-Joel-Grus/dp/1492041130/ref=sr_1_5?keywords=data+science&qid=1636616265&sr=8-5'}
# ]


# @app.route('/', methods=['GET'])
# def home():
#     return '''<h1>Data Science Library Reference</h1>
# <p>A test web service for accessing a libray of data science books and manuals.</p>'''


# # A route to return all of the available entries in our catalog.
# @app.route('/api/v1/resources/books/all', methods=['GET'])
# def api_all():
#     return jsonify(data_science_books)

# app.run()

