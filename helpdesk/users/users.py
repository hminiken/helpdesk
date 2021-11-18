import os
import random
from flask import Flask, Blueprint, render_template, request, redirect, url_for
from flask.helpers import flash
from flask_login import current_user, login_user, logout_user
from flask_login.utils import login_required
from helpdesk.users.models import LoginForm, RegistrationForm, UpdateProfileForm, Users
from werkzeug.urls import url_parse
from app import db
from datetime import datetime
# from flask_uploads import UploadSet, configure_uploads, IMAGES

from helpdesk.users.users_utils import  get_my_assigned_tickets, get_my_watched_tickets, get_my_watched_tickets_updates

users_bp = Blueprint('users_bp', __name__, 
                        template_folder='templates', 
                        static_folder='static')


@login_required
@users_bp.route("/")
def user():
    # get watched tickets
    assigned = get_my_assigned_tickets()
    watched = get_my_watched_tickets()
    updates = get_my_watched_tickets_updates()

    current_user.last_login = datetime.now()
    db.session.commit()

    # Get user ticket data
    return render_template('users/profile.html', watched=watched, updates=updates, assigned=assigned)


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
                    fname=form.fname.data, lname=form.lname.data, FK_role_id=form.permission.data.id, 
                    user_img=imgString)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('users_bp.user'))
    return render_template('users/admin_add_user.html', title='Register', form=form)



@users_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('users_bp.login'))


# photos = UploadSet('photos', IMAGES)

@users_bp.route("/edit_profile",  methods=['GET', 'POST'])
def edit_profile():

    # update_user = Users(email=current_user.email, fname=current_user.fname, lname=current_user.lname, 
    #                     ticket_created_updates=current_user.ticket_created_updates,
    #                     ticket_assigned_updates=current_user.ticket_assigned_updates, 
    #                     ticket_watched_updates=current_user.ticket_watched_updates)

    form = UpdateProfileForm()

    if request.method == 'GET':
        form.email.data=current_user.email
        form.fname.data=current_user.fname
        form.lname.data=current_user.lname        
        form.email_created.data=current_user.ticket_created_updates
        form.email_assigned.data=current_user.ticket_assigned_updates
        form.email_watched.data=current_user.ticket_watched_updates

 
    
    if form.validate_on_submit():

        user = Users.query.filter_by(email=current_user.email).first()
        assets_dir = '/static/images/avatars/'

        if form.user_img.data.filename != '':
            filename = 'profileImg' + str(current_user.user_id) + '.jpg'
            img = form.user_img.data
            img.save(os.path.dirname(__file__) + assets_dir + '/' + filename)        
            user.user_img = filename

        user.email=form.email.data
        user.fname=form.fname.data
        user.lname=form.lname.data
        user.ticket_created_updates=form.email_created.data
        user.ticket_assigned_updates=form.email_assigned.data 
        user.ticket_watched_updates = form.email_watched.data

        db.session.commit()
        return redirect(url_for('users_bp.user'))

    return render_template('users/edit_profile.html', form=form)
