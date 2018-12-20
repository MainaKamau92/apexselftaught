# app/employer/views.py

from flask import render_template, url_for, flash, redirect, request
from flask_login import login_required, current_user
import secrets
from PIL import Image
import os
from . import employer
from .. import db
from .. import create_app
from .forms import UpdateForm, PostJobForm
from ..models import JobPost


def save_picture(form_picture):
    """
    function for saving the path to the profile picture
    """
    app = create_app(config_name=os.getenv('APP_SETTINGS'))
    # random hex to be usedin storing the file name to avoid clashes
    random_hex = secrets.token_hex(8)
    # split method for splitting the filename from the file extension
    _, pic_ext = os.path.split(form_picture.filename)
    # pic_fn = picture filename which is a concatanation of the filename(hex name) and file extension
    pic_fn = random_hex + pic_ext
    # path to picture from the root to the profile_pics folder
    pic_path = os.path.join(app.root_path, 'static/profile_pics', pic_fn)
    output_size = (128, 128)
    img = Image.open(form_picture)
    img.thumbnail(output_size)
    img.save(pic_path)  # save the picture path to the file system
    return pic_fn


@employer.route('/employer/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    """
    Render the homepage template on the / route
    """
    jobs = JobPost.query.all()
    form = UpdateForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash(f'Account information updated', 'success')
        return redirect(url_for('employer.dashboard'))
    elif request.method == 'GET':
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static',
                         filename='profile_pics/' + current_user.image_file)
    return render_template('employer/dashboard.html', title='Employer',
                           image_file=image_file, form=form, jobs=jobs)


@employer.route('/employer/post/new', methods=['GET', 'POST'])
@login_required
def post_job():
    """
    Render the homepage template on the / route
    """
    form = PostJobForm()
    if form.validate_on_submit():
        job = JobPost(
            job_title=form.job_title.data,
            job_description=form.job_description.data,
            job_requirements=form.job_requirements.data,
            expected_pay=form.expected_pay.data,
            contact_email=form.contact_email.data,
            contact_number=form.contact_number.data,
            poster=current_user
        )
        db.session.add(job)
        db.session.commit()
        flash(f'You have posted a job succesfully', 'success')

        # redirect to employers dashboard

        return redirect(url_for('employer.dashboard'))
    # load job posting form
    return render_template('employer/post_job.html', title='New Job', form=form)


# @employer.route('/employer/jobs', methods=['GET', 'POST'])
# @login_required
# def job_posts():
   
#     return render_template('employer/dashboard.html', jobs=jobs)
