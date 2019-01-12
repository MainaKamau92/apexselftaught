# app/freelancer/views.py

from flask import render_template
from flask_login import login_required
from datetime import datetime
from flask import render_template, abort, url_for, flash, redirect, request
from flask_login import login_required, current_user
import os

# local imports
from .. import db
from .. import create_app
from ..models import Resume, Project, User
from ..employer.views import save_picture
from . import freelancer
from .forms import UpdateForm, ResumeForm, ProjectForm


def date():
    now = datetime.now()
    return now


def check_freelancer():
    """
    Prevent non freelancers from accessing views by employers from accessing this page
    """

    if not current_user.is_freelancer:
        abort(403)


@freelancer.route('/freelancer/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    """
    Render the homepage template on the / route
    """
    check_freelancer()
    user = User.query.filter_by(username=current_user.username).first_or_404()
    resume = Resume.query.filter_by(author=user).all()
    projects = Project.query.filter_by(architect=user).all()
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
        return redirect(url_for('freelancer.dashboard'))
    elif request.method == 'GET':
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static',
                         filename='profile_pics/' + current_user.image_file)
    return render_template('freelancer/dashboard.html', title='Freelancer',
                           date=date(), image_file=image_file, form=form,
                           resume=resume, projects=projects)


@freelancer.route('/freelancer/resume', methods=['GET', 'POST'])
@login_required
def post_resume():
    """
    Render the homepage template on the / route
    """
    check_freelancer()
    form = ResumeForm()
    if form.validate_on_submit():
        resume = Resume(
            description=form.description.data,
            tools=form.tools.data,
            experience=form.experience.data,
            skills=form.skills.data,
            author=current_user
        )
        db.session.add(resume)
        db.session.commit()
        flash(f'You have posted your resume succesfully', 'success')

        # redirect to freelancer's dashboard
        return redirect(url_for('freelancer.dashboard'))
    # load job posting form
    return render_template('freelancer/resume.html', title='Resume', form=form)


@freelancer.route('/freelancer/<int:res_id>/resume/update', methods=['GET', 'POST'])
@login_required
def update_resume(res_id):
    check_freelancer()
    user = User.query.filter_by(username=current_user.username).first()
    res_id = user.id
    res = Resume.query.filter_by(user_id=res_id).first()
    if res.author != current_user:
        abort(403)
    form = ResumeForm()
    if form.validate_on_submit():
        res.description = form.description.data
        res.tools = form.tools.data
        res.experience = form.experience.data
        res.skills = form.skills.data
        db.session.commit()
        flash(f'Your Resume has been updated', 'success')
        return redirect(url_for('freelancer.dashboard'))
    elif request.method == 'GET':
        form.description.data = res.description
        form.tools.data = res.tools
        form.experience.data = res.experience
        form.skills.data = res.skills

    return render_template('freelancer/resume.html', title='Update Resume', form=form)


@freelancer.route('/freelancer/projects', methods=['GET', 'POST'])
@login_required
def post_project():
    """
    Render the homepage template on the / route
    """
    check_freelancer()
    form = ProjectForm()
    if form.validate_on_submit():
        resume = Project(
            title=form.title.data,
            tools_used=form.tools_used.data,
            description=form.description.data,
            client=form.client.data,
            url_link=form.url_link.data,
            architect=current_user
        )
        db.session.add(resume)
        db.session.commit()
        flash(f'You added a project succesfully', 'success')

        # redirect to freelancer's dashboard
        return redirect(url_for('freelancer.dashboard'))
    # load job posting form
    return render_template('freelancer/projects.html', title='Project', form=form)


@freelancer.route('/freelancer/projects/<int:project_id>')
@login_required
def project(project_id):
    project = Project.query.get_or_404(project_id)
    return render_template('freelancer/project.html', title=project.title, project=project)


@freelancer.route('/freelancer/<int:project_id>/project/update', methods=['GET', 'POST'])
@login_required
def update_project(project_id):
    check_freelancer()
    project = Project.query.get_or_404(project_id)
    if project.architect != current_user:
        abort(403)
    form = ProjectForm()
    if form.validate_on_submit():
        project.title = form.title.data
        project.tools_used = form.tools_used.data
        project.description = form.description.data
        project.client = form.client.data
        project.url_link = form.url_link.data
        db.session.commit()
        flash(f'Your Project has been updated', 'success')
        return redirect(url_for('freelancer.project', project_id=project.id))
    elif request.method == 'GET':
        form.title.data = project.title
        form.tools_used.data = project.tools_used
        form.description.data = project.description
        form.client.data = project.client
        form.url_link.data = project.url_link
    return render_template('freelancer/projects.html', title='Update Project', form=form)


@freelancer.route('/freelancer/project/<int:project_id>/delete', methods=['POST'])
@login_required
def delete_project(project_id):
    check_freelancer()
    project = Project.query.get_or_404(project_id)
    if project.architect != current_user:
        abort(403)
    db.session.delete(project)
    db.session.commit()
    flash(f'Your Project has been deleted', 'success')
    return redirect(url_for('freelancer.dashboard'))


@freelancer.route('/freelancers', methods=['GET', 'POST'])
@login_required
def freelancers():
    page = request.args.get('page', 1, type=int)
    freelancers = User.query.filter_by(is_freelancer=True).order_by(
        User.id.desc()).paginate(page=page, per_page=5)
    resumes = Resume.query.all()
    return render_template('freelancer/freelancers.html', resumes=resumes, freelancers=freelancers, title="Apex | Freelancers")


@freelancer.route('/freelancers/<int:freelancer_id>')
@login_required
def get_freelancer(freelancer_id):
    user = User.query.filter_by(id=freelancer_id).first()
    res_by_id = Resume.query.filter_by(user_id=freelancer_id).first()
    proj_by_id = Project.query.filter_by(architect=user).all()
    return render_template('freelancer/freelancer.html', res_by_id=res_by_id,
                           proj_by_id=proj_by_id, title="Freelancer")
