#  https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-v-user-logins

from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from app import login

class User(UserMixin, db.Model):
    # primary keys are required by SQLAlchemy
    user_id = db.Column(db.Integer, primary_key=True)
    FK_role_id = db.Column(db.Integer)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    fname = db.Column(db.String(1000))
    lname = db.Column(db.String(1000))
    user_img = db.Column(db.String(1000))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))





from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')