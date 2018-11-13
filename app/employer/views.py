# app/employer/views.py

from flask import render_template
from flask_login import login_required

from . import employer


@employer.route('/employer/dashboard')
@login_required
def dashboard():
    """
    Render the homepage template on the / route
    """
    return render_template('employer/dashboard.html', title='Employer')
