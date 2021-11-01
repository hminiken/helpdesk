from flask import Flask, Blueprint, render_template, request, redirect, url_for
from flask_login import current_user, login_user
from werkzeug.security import generate_password_hash, check_password_hash

from helpdesk.users.users_utils import add_new_user, get_user_login_info

users_bp = Blueprint('users_bp', __name__, 
                        template_folder='templates', 
                        static_folder='static')


@users_bp.route("/")
def user():
    return render_template('users/profile.html')


@users_bp.route("/login")
def login():
    return render_template('users/login.html')


@users_bp.route("/log_user_in", methods=['POST'])
def log_user_in():
    email = request.form.get('login-email')
    password = request.form.get('login-password')

    user = get_user_login_info(email)

    if not user or not check_password_hash(user[0]['password'], password):
        # flash('Please check your login details and try again.')
        # if the user doesn't exist or password is wrong, reload the page
        return redirect(url_for('users_bp.login'))

    return redirect(url_for('users_bp.user'))



@users_bp.route("/logout")
def logout():
    # return render_template('users/login.html')
    return 'Logout'


@users_bp.route("/add_user")
def add_user():
    # return render_template('users/login.html')
    return render_template('users/admin_add_user.html')


@users_bp.route("/submit_user", methods=['POST'])
def submit_user():
    # return render_template('users/login.html')
    email = request.form.get('newuser-email')
    emp_id = request.form.get('newuser-emp-id')
    fname = request.form.get('newuser-fname')
    lname = request.form.get('newuser-lname')
    role = request.form.get('role-select')
    


    add_new_user(email, emp_id, fname, lname, role)
    return redirect(url_for('users_bp.user'))
