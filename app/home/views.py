# app/home/views.py

from flask import render_template, abort
from flask_login import current_user, login_required
from ..models import User

from . import home


@home.route('/')
def homepage():
    """
    Render the homepage template on the / route
    """
    return render_template('home/index.html', title='Welcome')


@home.route('/contact')
def contact():
    return render_template('contactus/contact_us.html', title='Contact Us')
