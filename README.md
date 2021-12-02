
# Help Desk

A ticketing system to create and manage a list of internal company problems. 

## What It Does
- Ticket creation, routing, categorization, and tagging
- Tracking and measurement of ticket metrics



## How to Start
Remote into the qea-engineering tickets server. Username and password are required. 

Navigate to the folder
>cd helpdesk

Activate the python virtual environment
>source myprojectenv/bin/activate

Verify if any gunicorn tasks are running and kill them as required.
>px ax|grep gunicorn
>
>pkill gunicorn

Start up the app with
>gunicorn --workers 1 --threads 3 -b 0.0.0.0:5000 wsgi:app


### Troubleshooting
- Conneciton Time Out:
  - Clear the iptable 
  - Try adding port 5000

## Requirements
An ubuntu server running version 20.04 or greater. 

### Modules Required
Required modules can be installed using requirements.txt, or by using pip install on the items listed below:
- cryptography
- DateTime
- email-validator
- Flask
- Flask-Login
- Flask-Mail
- Flask-MySQL
- Flask-SQLAlchemy
- Flask-Uploads
- Flask-WTF
- gunicorn
- Jinja2
- mysql
- mysqlclient
- pep517
- pip
- pymssql
- PyMySQL
- pyngrok
- pyodbc
- pytz
- SQLAlchemy
- sqlserverport
- Werkzeug
- wheel
- WTForms
- WTForms-JSON
- WTForms-SQLAlchemy


## Project Structure