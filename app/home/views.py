# app/home/views.py

from flask import render_template, abort, request
from flask_login import current_user, login_required
from ..models import User, BlogPost

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


@home.route('/blog')
def blog_post():
    page = request.args.get('page', 1, type=int)
    blogs = BlogPost.query.order_by(
        BlogPost.id.desc()).paginate(page=page, per_page=9)
    return render_template('home/blogs.html', blogs=blogs, title="Apex | Blogs")

@home.route('/blog/<int:blog_id>')
def get_blog(blog_id):
    blog = BlogPost.query.get_or_404(blog_id)
    #return render_template('employer/job.html', title=job.job_title, job=job)
    return render_template('home/blog.html', blog=blog, title="Apex | Blog")

@home.route('/about_us')
def about_us():
    return render_template('home/about_us.html', title='Apex | About Us')