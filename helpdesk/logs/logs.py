from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import current_user

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
@users_bp.route("/")
def logs():
    return
