from flask_wtf.form import FlaskForm
from wtforms.fields.choices import SelectField
from wtforms.fields.simple import StringField
from wtforms.validators import DataRequired
from database import db
from datetime import datetime


class dailyIDS(db.Model):
    # __bind_key__ = 'db3'
    id = db.Column(db.Integer, primary_key=True)
    created_by = db.Column(db.Integer)
    owner = db.Column(db.Integer)
    origin = db.Column(db.String(45))
    issue = db.Column(db.String(1000))
    notes = db.Column(db.String(1000))
    status = db.Column(db.String(45))
    work_stop = db.Column(db.String(45))
    date_due = db.Column(db.String(45))


    date_created = db.Column(db.DateTime(1000), nullable=False, default=datetime.now)
    date_entry = db.Column(db.DateTime(1000), nullable=False, default=datetime.now)


class IDSRowForm(FlaskForm):
    created_by = StringField('Employee ID', validators=[DataRequired()])
    owner = StringField('First Name', validators=[DataRequired()])
    issue = StringField('Last Name', validators=[DataRequired()])
    notes = StringField('Last Name', validators=[DataRequired()])
    status = StringField('Last Name', validators=[DataRequired()])
    work_stop = StringField('Last Name', validators=[DataRequired()])
    date_due = StringField('Last Name', validators=[DataRequired()])


    origin = SelectField('Origin', choices=[(1,'CFT'),(2,'Eng')])