# app/auth/form.py

from flask_wtf import FlaskForm
from wtforms import (PasswordField, StringField, SubmitField,
                     BooleanField, ValidationError, SelectField)
from wtforms.validators import Required, Email, EqualTo, Length

from ..models import User


class RegistrationForm(FlaskForm):
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
    employer = BooleanField('Employer')
    freelancer = BooleanField('Freelancer')
    password = PasswordField('Password', validators=[Required()])
    confirm_password = PasswordField('Confirm Password', validators=[
                                     Required(), EqualTo('password')])
    submit = SubmitField('Submit', render_kw={'class': 'btn btn-warning'})

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already exists')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already exists')


class LoginForm(FlaskForm):
    """
    Forms for logging in a user
    """
    email = StringField('Email', validators=[Required(), Email()], render_kw={
        'placeholder': 'email'})
    password = PasswordField('Password', validators=[Required()], render_kw={
                             'placeholder': '*********'})
    remember = BooleanField('Remember Me', render_kw={'class': 'remember'})
    submit = SubmitField('Log In')


class RequestResetForm(FlaskForm):
    """
    Password reset request form
    """
    email = StringField('Email', validators=[Required(), Email()], render_kw={
        'placeholder': 'email'})
    submit = SubmitField('Request Reset Password')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError(
                'There is no account with that email.Register first.')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[Required()])
    confirm_password = PasswordField('Confirm Password', validators=[
                                     Required(), EqualTo('password')])
    submit = SubmitField('Reset Password')
