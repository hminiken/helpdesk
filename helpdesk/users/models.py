#  https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-v-user-logins

from flask import app
from wtforms.fields.core import IntegerField, SelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, required
from app import db
from app import login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from wtforms.ext.sqlalchemy.fields import QuerySelectField


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

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


@login.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))






from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField('Employee ID', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class Permissions(UserMixin, db.Model):
    # primary keys are required by SQLAlchemy
    id = db.Column(db.Integer, primary_key=True)
    permission_role = db.Column(db.String(100))
    # permission_description = db.Column(db.String(1000))
    # permission_level = db.Column(db.Integer)
    # permission_department = db.Column(db.String(1000))


def skill_level_choices():
    data = db.session.query(Permissions).all()
    # data = Permissions.query.filter_by().all()

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
    # permission = SelectField('User Type', choices=[
    #     ('1', 'Admin'), 
    #     ('3', 'Eng. Admin'), 
    #     ('4', 'Eng. User'), 
    #     ('5', 'CAM Admin'),
    #     ('6', 'CAM User')
    #     ], validators=[DataRequired()])

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


