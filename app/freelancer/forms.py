from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import (PasswordField, StringField, SubmitField,
                     BooleanField, ValidationError, SelectField,
                     FieldList, TextAreaField)
from wtforms.validators import Required, Email, EqualTo, Length
from flask_login import current_user
from ..models import User


class UpdateForm(FlaskForm):
    """
    Form for users to create new account
    """
    first_name = StringField('First Name', validators=[Required()], render_kw={
                             'placeholder': 'first name'})
    last_name = StringField('Last Name', validators=[Required()], render_kw={
        'placeholder': 'last name'})
    username = StringField('Username', validators=[Required(), Length(
        min=2, max=15)], render_kw={'placeholder': 'username'})
    email = StringField('Email', validators=[Required(), Email()], render_kw={
                        'placeholder': 'email'})
    picture = FileField('Update Profile', validators=[
                        FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Username already exists')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Email already exists')


class ResumeForm(FlaskForm):
    """
    Form for users to create new account
    """
    description = TextAreaField('Describe yourself', validators=[Required()],
                                render_kw={'rows': '14', 'placeholder': 'Markdown supported'})
    tools = TextAreaField('Tools you use to work', validators=[Required()],
                          render_kw={'rows': '14', 'placeholder': 'Software Developer(eg, python language)'})
    experience = TextAreaField("Projects you've done", validators=[Required()],
                               render_kw={'rows': '14', 'placeholder': "Markdown is supported in formatting response"})
    skills = TextAreaField('Skills you have', validators=[Required()],
                           render_kw={'rows': '14', 'placeholder': "Markdown is supported in formatting response"})
    submit = SubmitField('Add')


class ProjectForm(FlaskForm):
    """
    Form for users to create new account
    """
    title = StringField('Project Title', validators=[Required()],
                        render_kw={'placeholder': 'e.g Web Application, Logo Design'})
    tools_used = TextAreaField('Tools Used (e.g, coding language, design software)', validators=[Required()],
                               render_kw={'rows': '14', 'placeholder': "Markdown is supported in formatting response"})
    description = TextAreaField('Project Description (Describe briefly what project entailed)', validators=[Required()],
                                render_kw={'rows': '14', 'placeholder': "Markdown is supported in formatting response"})
    client = StringField('Project Owners (Who was the project for?)', validators=[Required()],
                         render_kw={'placeholder': 'Company ABC'})
    url_link = StringField('Project URL', validators=[Required()],
                           render_kw={'placeholder': 'http://gh-pages.github.io'})
    submit = SubmitField('Submit')
