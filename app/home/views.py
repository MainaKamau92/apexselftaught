# app/home/views.py

from flask import render_template, abort
from flask_login import current_user, login_required

from . import home


@home.route('/')
def homepage():
    """
    Render the homepage template on the / route
    """
    return render_template('home/index.html', title='Welcome')


@home.route('/admin/dashboard')
@login_required
def admin_dashboard():
    # prevent non admins from accessing route
    if not current_user.is_admin:
        abort(403)
    return render_template('home/admin_dashboard.html', title='Admin Dashboard')

@home.route('/contact')
def contact():
    return render_template('contactus/contact_us.html', title='Contact Us')
