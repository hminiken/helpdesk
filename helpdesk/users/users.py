import random
from flask import Flask, Blueprint, render_template, request, redirect, url_for
from flask.helpers import flash
from flask_login import current_user, login_user, logout_user
from flask_login.utils import login_required
from werkzeug.security import generate_password_hash, check_password_hash
from helpdesk.users.models import LoginForm, RegistrationForm, Users
from werkzeug.urls import url_parse
from app import db

from helpdesk.users.users_utils import add_new_user, get_user_login_info

users_bp = Blueprint('users_bp', __name__, 
                        template_folder='templates', 
                        static_folder='static')


@login_required
@users_bp.route("/")
def user():
    # Get user ticket data
    return render_template('users/profile.html')


@users_bp.route("/login",  methods=['GET', 'POST'])
def login():
    form = LoginForm()
    # if form.validate_on_submit():
    #     flash('Login requested for user {}, remember_me={}'.format(
    #         form.username.data, form.remember_me.data))
    #     return redirect('/index')

    if form.validate_on_submit():
        user = Users.query.filter_by(user_id=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('users_bp.login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('users_bp.user')
        return redirect(next_page)

    return render_template('users/login.html', form=form)




# @users_bp.route("/log_user_in", methods=['POST'])
# def log_user_in():
#     email = request.form.get('login-email')
#     password = request.form.get('login-password')

#     user = get_user_login_info(email)

#     if not user or not check_password_hash(user[0]['password'], password):
#         # flash('Please check your login details and try again.')
#         # if the user doesn't exist or password is wrong, reload the page
#         return redirect(url_for('users_bp.login'))

#     return redirect(url_for('users_bp.user'))



# @users_bp.route("/logout")
# def logout():
#     # return render_template('users/login.html')
#     return 'Logout'


@users_bp.route("/add_user",  methods=['GET', 'POST'])
def add_user():
    # if current_user.is_authenticated:
    #     return redirect(url_for('users_bp.user'))

    default_imgs = ['default1.png', 'default2.png',
                    'default3.png', 'default4.png', 'default5.png']

    imgString = random.choice(default_imgs)

    form = RegistrationForm()
    if form.validate_on_submit():
        user = Users(user_id=form.user_id.data, email=form.email.data, 
                    fname=form.fname.data, lname=form.lname.data, FK_role_id=form.permission.data, 
                    user_img=imgString)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('users_bp.user'))
    return render_template('users/admin_add_user.html', title='Register', form=form)

    # return render_template('users/login.html')
    # return render_template('users/admin_add_user.html', form=form)


@users_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('users_bp.login'))

# @users_bp.route("/submit_user", methods=['POST'])
# def submit_user():
#     # return render_template('users/login.html')
#     email = request.form.get('newuser-email')
#     emp_id = request.form.get('newuser-emp-id')
#     fname = request.form.get('newuser-fname')
#     lname = request.form.get('newuser-lname')
#     role = request.form.get('role-select')
    


#     add_new_user(email, emp_id, fname, lname, role)
#     return redirect(url_for('users_bp.user'))
