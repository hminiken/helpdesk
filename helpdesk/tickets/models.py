'''
* Author: Hillary Miniken
* Email: hminiken@outlook.com
* Date Created: 2021-11-18
* Filename: models.py
*
* Description: for use with SQLAlchemy, the ticket classes and the 
               forms that allow the database to be updated
'''

from wtforms_sqlalchemy.fields import QuerySelectField
from flask_login.mixins import UserMixin
from wtforms import StringField, BooleanField, SubmitField, IntegerField, SelectField
from flask_wtf import FlaskForm
from datetime import datetime
# from wtforms.fields.core import IntegerField, SelectField
from wtforms.fields.simple import TextAreaField
from wtforms.validators import DataRequired, Length, Optional
import wtforms_sqlalchemy
from database import db
from database import conn_erp


class TicketUpdates(db.Model):
    ticket_update_id = db.Column(db.Integer, primary_key=True)
    FK_ticket_id = db.Column(db.Integer)
    update_user = db.Column(db.Integer)
    update_description = db.Column(db.String(1000))
    update_date = db.Column(db.DateTime(
        1000), nullable=False, default=datetime.now)
    id = ticket_update_id


class Tickets(db.Model):
    ticket_id = db.Column(db.Integer, primary_key=True)
    priority = db.Column(db.Integer)
    description = db.Column(db.String(1000))
    created_by = db.Column(db.Integer)
    date_created = db.Column(db.DateTime(
        1000), nullable=False, default=datetime.now)
    assigned_to = db.Column(db.Integer)
    customer = db.Column(db.String(1000))
    assembly = db.Column(db.Integer)
    part_number = db.Column(db.String(1000))
    work_order = db.Column(db.String(1000))
    category = db.Column(db.String(1000))
    subcategory = db.Column(db.String(1000))
    attachments = db.Column(db.String(1000))
    closed_by = db.Column(db.Integer)
    date_closed = db.Column(db.DateTime(
        1000), nullable=False, default=datetime.now)
    id = ticket_id

   
class Category(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(100))


class Subcategory(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    FK_category_id = db.Column(db.Integer, primary_key=True)
    subcategory_name = db.Column(db.String(100))


def customer_choices():
    cursor_unipoint = conn_erp()
    cust_query = '''
                SELECT Customer.CUS_CustomerID  as id, Customer.CUS_SortRef as customer, Customer.CUS_ActiveFlag
                FROM 
                Customer
                WHERE Customer.CUS_SortRef Not Like 'QX%';
                '''

    cust_list = []
    result = cursor_unipoint.execute(cust_query).fetchall()
    for row in result:
        cust_list.append(row)

    # Create the list for the dropdown in the format ZZZ - Customer Name
    data = []
    data.append((0, "000 - Not Applicable or Many"))
    i = 0
    for item in cust_list:
        if item[0].isnumeric() and item[2] == True:
            data.append((int(item[0]), item[0] + " - " + item[1]))
            i = i + 1

    return data


def category_choices():
    data = db.session.query(Category).all()
    return data



class TicketCommentForm(FlaskForm):
    comment = TextAreaField('Status Update', validators=[DataRequired()])
    ticket_id = IntegerField(validators=[DataRequired()])



class NewTicketForm(FlaskForm):
    data = customer_choices()
    assembly = StringField('Assembly', validators=[
                           DataRequired(), Length(max=100)])
    priority = BooleanField('Priority')
    workorder = StringField('Work Order(s)', validators=[
                            DataRequired(), Length(max=100)])
    description = TextAreaField('Description', validators=[
                                DataRequired(), Length(max=1000)])
    partnumber = StringField('Part Numbers', validators=[
                             DataRequired(), Length(max=100)])
    customer = SelectField('User Type', choices=data,
                           validators=[DataRequired()])
    category = QuerySelectField('Category',   validators=[DataRequired(
                                )], query_factory=category_choices, get_label='category_name')
    subcat = SelectField('SubCategory',  coerce=int, validators=[
                         Optional()], choices=[], validate_choice=False)
    submit = SubmitField('Create Ticket')







   