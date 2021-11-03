from wtforms import StringField, PasswordField, BooleanField, SubmitField
from flask_wtf import FlaskForm
from datetime import datetime
from wtforms.fields.core import IntegerField
from wtforms.fields.simple import TextAreaField

from wtforms.validators import DataRequired
from app import db


class TicketUpdates(db.Model):
    # primary keys are required by SQLAlchemy
    ticket_update_id = db.Column(db.Integer, primary_key=True)
    FK_ticket_id = db.Column(db.Integer)
    update_user = db.Column(db.Integer)
    update_description = db.Column(db.String(1000))
    update_date = db.Column(db.DateTime(
        1000), nullable=False, default=datetime.now)
    id = ticket_update_id


class TicketCommentForm(FlaskForm):
    comment = TextAreaField('Status Update', validators=[DataRequired()])
    ticket_id = IntegerField(validators=[DataRequired()])
    # ticket_id = PasswordField('Status Update', validators=[DataRequired()])
    # submit = SubmitField('Submit', )
