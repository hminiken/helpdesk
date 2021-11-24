#  https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-v-user-logins

from datetime import datetime
from flask import app
from wtforms.fields.simple import FileField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from database import db
from database import login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from wtforms_sqlalchemy.fields import QuerySelectField

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class Users(UserMixin, db.Model):
    # primary keys are required by SQLAlchemy
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    FK_role_id = db.Column(db.Integer)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    fname = db.Column(db.String(1000))
    lname = db.Column(db.String(1000))
    user_img = db.Column(db.String(1000))
    last_login = db.Column(db.DateTime(
        1000), nullable=False, default=datetime.now())
    ticket_created_updates = db.Column(db.Integer)
    ticket_assigned_updates = db.Column(db.Integer)
    ticket_watched_updates = db.Column(db.Integer)


    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


@login.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


class UpdateProfileForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    fname = StringField('First Name', validators=[DataRequired()])
    lname = StringField('Last Name', validators=[DataRequired()])
    user_img = FileField('')
    email_created = BooleanField('Tickets I created')
    email_assigned = BooleanField('Tickets I am assigned to')
    email_watched = BooleanField('Tickets I am watching')
    submit = SubmitField('Update Profile')






class LoginForm(FlaskForm):
    username = StringField('Employee ID', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class Permissions(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    permission_role = db.Column(db.String(100))


def skill_level_choices():
    data = db.session.query(Permissions).all()

    choices = []
    for item in data:
        pair = (item.id, item.permission_role)
        choices.append(pair)

    return data



class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    user_id = StringField('Employee ID', validators=[DataRequired()])
    fname = StringField('First Name', validators=[DataRequired()])
    lname = StringField('Last Name', validators=[DataRequired()])

    permission = QuerySelectField(u'User Type',
                                   validators=[DataRequired()],
                                  query_factory=skill_level_choices, get_label='permission_role')
                                #   choices=[(g.id, g.permission_role) for g in data])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = Users.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, user_id):
        user = Users.query.filter_by(user_id=user_id.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')
        else:
            return True


