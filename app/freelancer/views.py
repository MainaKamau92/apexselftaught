# app/freelancer/views.py

from flask import render_template
from flask_login import login_required


from . import freelancer


@freelancer.route('/freelancer/dashboard')
@login_required
def dashboard():
    """
    Render the homepage template on the / route
    """
    return render_template('freelancer/dashboard.html', title='Freelancer')
