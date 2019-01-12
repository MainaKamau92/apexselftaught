from . import admin
from flask import abort, render_template, flash, redirect, url_for
from flask_login import current_user, login_required

from ..models import User, JobPost


def check_admin():
    """
    Prevent non-admins from accessing this page
    """

    if not current_user.is_admin:
        abort(403)


@admin.route('/dashboard')
@login_required
def admin_dashboard():
    # prevent non admins from accessing route
    check_admin()
    users = User.query.all()
    return render_template('admin/admin_dashboard.html', users=users)


@admin.route('/employers')
@login_required
def employers():
    check_admin()
    employers = User.query.filter_by(is_employer=True).all()
    return render_template('admin/employers.html', employers=employers)


@admin.route('/freelancers')
@login_required
def freelancers():
    check_admin()
    freelancers = User.query.filter_by(is_freelancer=True).all()
    return render_template('admin/freelancers.html', freelancers=freelancers)


@admin.route('/delete/<int:id>', methods=['POST'])
def delete_user(id):
    from app import db
    """
    Delete a user
    """
    check_admin()
    user = User.query.get_or_404(id)
    if user.is_admin:
        flash(f'You cannot remove an admin user', 'warning')
        abort(403)
    db.session.delete(user)
    db.session.commit()
    flash(f'You have successfully deleted a user', 'success')
    return redirect(url_for('admin.admin_dashboard'))
