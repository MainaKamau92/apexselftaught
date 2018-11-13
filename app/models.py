from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


from app import db, login_manager


class User(UserMixin, db.Model):
    """
    Class for creating user tables on db
    """

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(250), index=True, unique=True, nullable=False)
    username = db.Column(db.String(100), index=True,
                         unique=True, nullable=False)
    first_name = db.Column(db.String(50), index=True, nullable=False)
    last_name = db.Column(db.String(50), index=True, nullable=False)
    password_hash = db.Column(db.String(128))
    image_file = db.Column(db.String(20), nullable=False,
                           default='default.jpg')
    is_freelancer = db.Column(db.Boolean, default=False)
    is_employer = db.Column(db.Boolean, default=False)
    is_admin = db.Column(db.Boolean, default=False)
    resume_id = db.Column(db.Integer, db.ForeignKey('resumes.id'))
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'))
    jobpost_id = db.Column(db.Integer, db.ForeignKey('jobposts.id'))

    @property
    def password(self):
        """
        Prevent password from being accesssed
        """
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        """
        Set password to a hashed password
        """
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """
        Check if hashed password matches actual one
        """
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User: {}>'.format(self.username)

# set up a user loader


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class Resume(db.Model):
    """
    Class creates tables for freelancer resume
    """

    __tablename__ = 'resumes'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    tools = db.Column(db.Text, nullable=False)
    experience = db.Column(db.Text)
    skills = db.Column(db.Text)
    user = db.relationship('User', backref='resume', lazy='dynamic')


class Project(db.Model):
    """
    Class creates tables for freelancer resume
    """

    __tablename__ = 'projects'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    title = db.Column(db.String(100), nullable=False)
    tools_used = db.Column(db.Text)
    description = db.Column(db.Text)
    client = db.Column(db.String(100))
    user = db.relationship('User', backref='project', lazy='dynamic')


class JobPost(db.Model):
    """
    Class creates tables for jog postings by employer
    """

    __tablename__ = 'jobposts'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    job_title = db.Column(db.String(100), nullable=False)
    job_description = db.Column(db.Text, nullable=False)
    job_requirements = db.Column(db.Text, nullable=False)
    expected_pay = db.Column(db.Float)
    date_posted = db.Column(db.DateTime, nullable=False,
                            default=datetime.utcnow)
    contact_email = db.Column(db.String(150), nullable=False, unique=True)
    contact_number = db.Column(db.BigInteger, unique=True)
    user = db.relationship('User', backref='jobpost', lazy='dynamic')
