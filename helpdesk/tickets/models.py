from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
from app import db


class TicketUpdate(db.Model):
    # primary keys are required by SQLAlchemy
    ticket_update_id = db.Column(db.Integer, primary_key=True)
    FK_ticket_id = db.Column(db.Integer)
    update_user = db.Column(db.Integer)
    update_description = db.Column(db.String(1000))
    update_date = db.Column(db.Datetime(1000))
    id = ticket_update_id


class TicketCommentForm(FlaskForm):
    comment = PasswordField('Status Update', validators=[DataRequired()])
    submit = SubmitField('Sign In')
