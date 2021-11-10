from flask_login.mixins import UserMixin
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from flask_wtf import FlaskForm
from datetime import datetime
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.fields.core import IntegerField, SelectField
from wtforms.fields.simple import TextAreaField

from wtforms.validators import DataRequired
from wtforms.widgets.core import CheckboxInput
from app import db
from database import conn_erp, conn_unipoint


class TicketUpdates(db.Model):
    # primary keys are required by SQLAlchemy
    ticket_update_id = db.Column(db.Integer, primary_key=True)
    FK_ticket_id = db.Column(db.Integer)
    update_user = db.Column(db.Integer)
    update_description = db.Column(db.String(1000))
    update_date = db.Column(db.DateTime(
        1000), nullable=False, default=datetime.now)
    id = ticket_update_id


class Tickets(db.Model):
    # primary keys are required by SQLAlchemy
    ticket_id = db.Column(db.Integer, primary_key=True)
    priority = db.Column(db.Integer)
    description = db.Column(db.String(1000))
    created_by = db.Column(db.Integer)
    date_created = db.Column(db.DateTime(
        1000), nullable=False, default=datetime.now)
    assigned_to = db.Column(db.Integer)
    customer = db.Column(db.String(1000))
    assembly = db.Column(db.Integer)
    partnumber = db.Column(db.String(1000))
    workorder = db.Column(db.String(1000))
    category = db.Column(db.String(1000))
    subcategory = db.Column(db.String(1000))
    attachments = db.Column(db.String(1000))
    closed_by = db.Column(db.Integer)
    date_closed = db.Column(db.DateTime(
        1000), nullable=False, default=datetime.now)
    id = ticket_id

   

class TicketCommentForm(FlaskForm):
    comment = TextAreaField('Status Update', validators=[DataRequired()])
    ticket_id = IntegerField(validators=[DataRequired()])


def customer_choices():

    cursor_unipoint = conn_erp()

    task_query = '''
        SELECT Customer.CUS_CustomerID  as id, Customer.CUS_SortRef as customer, Customer.CUS_ActiveFlag
        FROM 
        Customer
     WHERE Customer.CUS_SortRef Not Like 'QX%';
        '''

    task_list = []

    result = cursor_unipoint.execute(task_query).fetchall()

    for row in result:
        # task_list.append([x for x in row])
        task_list.append(row)

    data = []
    data.append((0, "000 - Not Applicable or Many"))
    i = 0
    for item in task_list:
        if item[0].isnumeric() and item[2] == True:
            data.append((int(item[0]), item[0] + " - " + item[1]))
            # item[0] = int(item[0])
            i = i + 1

    return data


class Category(UserMixin, db.Model):
    # primary keys are required by SQLAlchemy
    id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(100))
    # permission_description = db.Column(db.String(1000))
    # permission_level = db.Column(db.Integer)
    # permission_department = db.Column(db.String(1000))


def category_choices():
    data = db.session.query(Category).all()  
    return data


class Subcategory(UserMixin, db.Model):
    # primary keys are required by SQLAlchemy
    id = db.Column(db.Integer, primary_key=True)
    FK_category_id = db.Column(db.String(100))
    subcategory_name = db.Column(db.String(100))


def subcategory_choices():
    data = db.session.query(Subcategory).all()
    return data




class NewTicketForm(FlaskForm):
    data = customer_choices()
    assembly = StringField('Assembly', validators=[DataRequired()])
    priority = BooleanField('Priority')
    workorder = StringField('Work Order(s)', validators=[DataRequired()])
    partnumber = StringField('Part Numbers', validators=[DataRequired()])
    customer = SelectField('User Type', choices=data,
                             validators=[DataRequired()])
    category = QuerySelectField('Category',   validators=[DataRequired()], query_factory=category_choices, get_label='category_name')
    subcat = SelectField('SubCategory', validators=[DataRequired(
    )])
    submit = SubmitField('Create Ticket')


   