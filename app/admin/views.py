from . import admin
from flask import abort, render_template, flash, redirect, url_for, request
from flask_login import current_user, login_required
from .forms import BlogForm, UpdateForm
from ..models import User, JobPost, BlogPost
from ..employer.views import date
import secrets
from PIL import Image
import os
from app import db, create_app



def check_admin():
    """
    Prevent non-admins from accessing this page
    """

    if not current_user.is_admin:
        abort(403)

def save_blog_picture(form_picture):
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
    pic_path = os.path.join(app.root_path, 'static/blog_pics', pic_fn)
    #output_size = (512, 512)
    img = Image.open(form_picture)
    #img.thumbnail(output_size)
    img.save(pic_path)  # save the picture path to the file system
    return pic_fn

@admin.route('/profile', methods=['GET', 'POST'])
@login_required
def admin_profile():
    """
    Render the homepage template on the / route
    """
    from ..employer.views import save_picture
    check_admin()
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=current_user.username).first_or_404()
    jobs = JobPost.query.filter_by(poster=user)\
        .order_by(JobPost.date_posted.desc()).\
        paginate(page=page, per_page=5)
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
        return redirect(url_for('admin.admin_profile'))
    elif request.method == 'GET':
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static',
                         filename='profile_pics/' + current_user.image_file)
    return render_template('admin/admin_profile.html', title=user.first_name + " " + user.last_name,
                           image_file=image_file, form=form, jobs=jobs, date=date())
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


@admin.route('/blog', methods=['GET', 'POST'])
@login_required
def blog():
      
    check_admin()
    form = BlogForm()
    if form.validate_on_submit():    
        if form.picture.data:
            picture_file = save_blog_picture(form.picture.data)                       
            blog = BlogPost(
                blog_title=form.blog_title.data,
                blog_description=form.blog_description.data,
                blogger=current_user,
                image_file=picture_file
            ) 
        blog = BlogPost(
            blog_title=form.blog_title.data,
            blog_description=form.blog_description.data,
            blogger=current_user
        )
        db.session.add(blog)
        db.session.commit()
        flash(f'You have posted a blog successfully', 'success')

        # redirect to admin dashboard

        return redirect(url_for('home.blog_post'))
    # load blog posting form
    return render_template('blog/blog.html', title="AST | Blog", form=form)


@admin.route('/blogs/<int:blog_id>/update', methods=['GET', 'POST'])
@login_required
def update_blog(blog_id):
    check_admin()
    blog = BlogPost.query.get_or_404(blog_id)
    if blog.blogger != current_user:
        abort(403)
    form = BlogForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_blog_picture(form.picture.data)
            blog.image_file = picture_file
        blog.blog_title = form.blog_title.data
        blog.blog_description = form.blog_description.data
        db.session.commit()
        flash(f'Your Blog has been updated', 'success')
        return redirect(url_for('home.get_blog', blog_id=blog.id))
    elif request.method == 'GET':
        form.blog_title.data = blog.blog_title
        form.blog_description.data = blog.blog_description

    return render_template('blog/blog.html', title='Update Blog', form=form)


@admin.route('/blogs/<int:blog_id>/delete', methods=['POST'])
@login_required
def delete_blog(blog_id):
    check_admin()
    blog = BlogPost.query.get_or_404(blog_id)
    if blog.blogger != current_user:
        abort(403)
    db.session.delete(blog)
    db.session.commit()
    flash(f'Your Blog has been deleted', 'success')
    return redirect(url_for('home.blog_post'))
