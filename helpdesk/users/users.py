import os
import random
from flask import Blueprint, render_template, request, redirect, url_for
from flask.helpers import flash
from flask_login import current_user, login_user, logout_user
from flask_login.utils import login_required
from helpdesk.users.models import LoginForm, RegistrationForm, UpdateProfileForm, Users
from werkzeug.urls import url_parse
from database import db
from datetime import datetime

from helpdesk.users.users_utils import  get_my_assigned_tickets, get_my_permissions, get_my_watched_tickets, get_my_watched_tickets_updates

users_bp = Blueprint('users_bp', __name__, 
                        template_folder='templates', 
                        static_folder='static')


# Reroute all unless already trying to log in
@users_bp.before_request
def before_request():
    if current_user.is_authenticated == False and request.endpoint != 'users_bp.login' and '/static/' not in request.path:
        return redirect(url_for('users_bp.login'))


'''
'''
@login_required
@users_bp.route("/")
def user():
    # get watched tickets
    assigned = get_my_assigned_tickets()
    watched = get_my_watched_tickets()
    updates = get_my_watched_tickets_updates()
    permission = get_my_permissions()

    # Get user ticket data
    return render_template('users/profile.html', watched=watched, updates=updates, assigned=assigned, permission=permission)

'''
'''
@users_bp.route("/login",  methods=['GET', 'POST'])
def login():
    form = LoginForm()
    
    if form.validate_on_submit():

        # Get user and validate their password
        user = Users.query.filter_by(user_id=form.username.data).first()
        if user is None:
            flash('Invalid username')
            return redirect(url_for('users_bp.login'))
        elif not user.check_password(form.password.data):
            flash('Invalid password')
            return redirect(url_for('users_bp.login'))
        
        # Log user with succesful
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('users_bp.user')
        return redirect(next_page)

    return render_template('users/login.html', form=form)


'''
'''
@users_bp.route("/reset_password",  methods=['GET', 'POST'])
def reset_password():
    form = LoginForm()
    form.submit.label.text = 'Reset Password'

    if form.validate_on_submit():
        user = Users.query.filter_by(user_id=current_user.user_id).first()

        if user.user_id != int(form.username.data):
            flash('Please enter your employee ID')
        elif form.password.data != form.passwordMatch.data:
            flash('Please verify passwords match')
        else:
            user.set_password(form.password.data)
            db.session.commit()
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('users_bp.user')
            return redirect(next_page)

    return render_template('users/reset_password.html', form=form)



'''
'''
@users_bp.route("/add_user",  methods=['GET', 'POST'])
def add_user():

    default_imgs = ['default1.png', 'default2.png',
                    'default3.png', 'default4.png', 'default5.png']

    imgString = random.choice(default_imgs)

    form = RegistrationForm()
    if form.validate_on_submit():
        user = Users(user_id=form.user_id.data, email=form.email.data, 
                    fname=form.fname.data, lname=form.lname.data, FK_role_id=form.permission.data.id, 
                    user_img=imgString)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('users_bp.user'))
    return render_template('users/admin_add_user.html', title='Register', form=form)


'''
'''
@users_bp.route('/logout')
def logout():
    current_user.last_login = datetime.now()
    db.session.commit()
    logout_user()
    return redirect(url_for('users_bp.login'))


'''
'''
@users_bp.route("/edit_profile",  methods=['GET', 'POST'])
def edit_profile():

    form = UpdateProfileForm()

    # When loading page, fetch current user information and load into the fields
    if request.method == 'GET':
        form.email.data=current_user.email
        form.fname.data=current_user.fname
        form.lname.data=current_user.lname        
        form.email_created.data=current_user.ticket_created_updates
        form.email_assigned.data=current_user.ticket_assigned_updates
        form.email_watched.data=current_user.ticket_watched_updates 
    
    # Update user on submit
    if form.validate_on_submit():
        user = Users.query.filter_by(email=current_user.email).first()
        assets_dir = '/static/images/avatars'

        # Update profile pic only if user uploaded a new profile image
        if form.user_img.data.filename != '':
            filename = 'profileImg' + str(current_user.user_id) + '.jpg'
            img = form.user_img.data
            img.seek(0)
            img.save(os.path.dirname(__file__) + assets_dir + '/' + filename)      
            img.close()  
            user.user_img = filename

        # Update user in database with new info
        user.email=form.email.data
        user.fname=form.fname.data
        user.lname=form.lname.data
        user.ticket_created_updates=form.email_created.data
        user.ticket_assigned_updates=form.email_assigned.data 
        user.ticket_watched_updates = form.email_watched.data

        db.session.commit()
        return redirect(url_for('users_bp.user'))

    return render_template('users/edit_profile.html', form=form)

'''
'''
@users_bp.route("/admin_edit_user",  methods=['GET', 'POST'])
def admin_edit_user():

    form = UpdateProfileForm()

    if request.method == 'GET':
        form.email.data = current_user.email
        form.fname.data = current_user.fname
        form.lname.data = current_user.lname
        form.email_created.data = current_user.ticket_created_updates
        form.email_assigned.data = current_user.ticket_assigned_updates
        form.email_watched.data = current_user.ticket_watched_updates

    if form.validate_on_submit():

        user = Users.query.filter_by(email=current_user.email).first()
        assets_dir = '/static/images/avatars/'

        if form.user_img.data.filename != '':
            filename = 'profileImg' + str(current_user.user_id) + '.jpg'
            img = form.user_img.data
            img.save(os.path.dirname(__file__) + assets_dir + '/' + filename)
            user.user_img = filename

        user.email = form.email.data
        user.fname = form.fname.data
        user.lname = form.lname.data
        user.ticket_created_updates = form.email_created.data
        user.ticket_assigned_updates = form.email_assigned.data
        user.ticket_watched_updates = form.email_watched.data

        db.session.commit()
        return redirect(url_for('users_bp.user'))

    return render_template('users/edit_profile.html', form=form)



'''
'''
@users_bp.route('/clear_ticket_updates', methods=['POST'])
def clear_ticket_updates():
    current_user.last_login = datetime.now()
    db.session.commit()

    return ""

