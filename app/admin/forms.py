
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, TextAreaField, ValidationError
from wtforms.validators import Required, Email, Length
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


class BlogForm(FlaskForm):
    """
    Forms for logging in a user
    """
    blog_title = StringField('Blog Title', validators=[Required()],
                            render_kw={'placeholder': 'Blog Title'})
    blog_description = TextAreaField('Blog Body', validators=[Required()],
                                    render_kw={'rows': '25', 
                                    'placeholder': "Use the '*' before you start the sentence to make a list",'id':'textbox'})
    picture = FileField('Blog Photo', validators=[
                        FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Submit')
