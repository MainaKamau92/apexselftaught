# app/employer/views.py

from flask import render_template, abort, url_for, flash, redirect, request
from flask_login import login_required, current_user
import secrets
from PIL import Image
import os
import click
from . import employer
from .. import db
from .. import create_app
from .forms import UpdateForm, PostJobForm
from ..models import JobPost, User
from datetime import datetime
import cloudinary

cloudinary.config(
  cloud_name=os.getenv('cloud_name'),
  api_key=os.getenv('api_key'),
  api_secret=os.getenv('api_secret')
)

def date():
    now = datetime.now()
    return now


def check_employer():
    """
    Prevent non employer from accessing views by employers from accessing this page
    """

    if not current_user.is_employer:
        abort(403)

def upload_profile_image(file):

    """
    Function to upload the profile image
    """
    import cloudinary.uploader
    upload_data = cloudinary.uploader.upload(file)
    return upload_data


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
    output_size = (512, 512)
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
    check_employer()
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=current_user.username).first_or_404()
    jobs = JobPost.query.filter_by(poster=user)\
        .order_by(JobPost.date_posted.desc()).\
        paginate(page=page, per_page=5)
    form = UpdateForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_url = upload_profile_image(form.picture.data)
            current_user.image_file = picture_url['secure_url']
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
    return render_template('employer/dashboard.html', title=user.first_name + " " + user.last_name,
                           image_file=current_user.image_file, form=form, jobs=jobs, date=date())


@employer.route('/employer/post/new', methods=['GET', 'POST'])
@login_required
def post_job():
    """
    Render the homepage template on the / route
    """
    check_employer()
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
        flash(f'You have posted a job successfully', 'success')

        # redirect to employers dashboard

        return redirect(url_for('employer.job_posts'))
    # load job posting form
    return render_template('employer/post_job.html', title='New Job', form=form)


@employer.route('/jobs', methods=['GET'])
@login_required
def job_posts():
    page = request.args.get('page', 1, type=int)
    jobs = JobPost.query.order_by(
        JobPost.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('employer/jobs.html', jobs=jobs, title="Apex | Jobs")


@employer.route('/employer/jobs/<int:job_id>')
@login_required
def job(job_id):
    job = JobPost.query.get_or_404(job_id)
    return render_template('employer/job.html', title=job.job_title, job=job)


@employer.route('/employer/jobs/<int:job_id>/update', methods=['GET', 'POST'])
@login_required
def update_job(job_id):
    check_employer()
    job = JobPost.query.get_or_404(job_id)
    if job.poster != current_user:
        abort(403)
    form = PostJobForm()
    if form.validate_on_submit():
        job.job_title = form.job_title.data
        job.job_description = form.job_description.data
        job.job_requirements = form.job_requirements.data
        job.expected_pay = form.expected_pay.data
        job.contact_email = form.contact_email.data
        job.contact_number = form.contact_number.data
        db.session.commit()
        flash(f'Your Job has been updated', 'success')
        return redirect(url_for('employer.job', job_id=job.id))
    elif request.method == 'GET':
        form.job_title.data = job.job_title
        form.job_description.data = job.job_description
        form.job_requirements.data = job.job_requirements
        form.expected_pay.data = job.expected_pay
        form.contact_email.data = job.contact_email
        form.contact_number.data = job.contact_number

    return render_template('employer/post_job.html', title='Update Job', form=form)


@employer.route('/employer/jobs/<int:job_id>/delete', methods=['POST'])
@login_required
def delete_job(job_id):
    check_employer()
    job = JobPost.query.get_or_404(job_id)
    if job.poster != current_user:
        abort(403)
    db.session.delete(job)
    db.session.commit()
    flash(f'Your Job has been deleted', 'success')
    return redirect(url_for('employer.job_posts'))


@employer.route('/jobs/<username>', methods=['GET', 'POST'])
@login_required
def user_jobs(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    jobs = JobPost.query.filter_by(poster=user)\
        .order_by(JobPost.date_posted.desc()).\
        paginate(page=page, per_page=5)
    return render_template('employer/user_jobs.html',
                           jobs=jobs, user=user, title="Apex | Jobs")
