import os
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from app import db, login_manager



secret = os.getenv('SECRET')
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
    image_file = db.Column(db.String(1000), nullable=False,
                           default='default.png')
    is_freelancer = db.Column(db.Boolean, default=False)
    is_employer = db.Column(db.Boolean, default=False)
    is_admin = db.Column(db.Boolean, default=False)
    resume = db.relationship('Resume', backref='author', lazy=True)
    project = db.relationship('Project', backref='architect', lazy=True)
    jobpost = db.relationship('JobPost', backref='poster', lazy=True)

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

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(secret, expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(secret)
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

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
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)


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
    url_link = db.Column(db.String(500))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)


class JobPost(db.Model):
    """
    Class creates tables for jog postings by employer
    """

    __tablename__ = 'jobposts'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    job_title = db.Column(db.String(100), nullable=False)
    job_description = db.Column(db.Text, nullable=False)
    job_requirements = db.Column(db.Text, nullable=False)
    expected_pay = db.Column(db.String(150))
    date_posted = db.Column(db.DateTime, nullable=False,
                            default=datetime.utcnow)
    contact_email = db.Column(db.String(150), nullable=False)
    contact_number = db.Column(db.String(150))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
