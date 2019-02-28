"""
This module deals with the creation of the forms that are to be used in the admin routes for various purposes
which include:
A form for writing the blog post of the application that includes a title and a body
A form for editing a blog post individually which also includes a title and a body
This forms can only be accessible to users with admin privileges
Implements FlaskForm module from the flask_wtf package that gives access to various inputs that are rendered 
on the template in their HTML correct formatting based on the description of the classes inherited from the FlaskForm module
e.g StringField() defines the equivalent of an input on an HTML format 
"""
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import Required, Email, Length
from flask_login import current_user
from ..models import User


class UpdateForm(FlaskForm):
    """
    Forms for admin users to edit blogs they have posted on the site
    The class inherits fromm the FlaskForm module which gives access to the TextArea(Renders a text field on the template)
    StringField(render an input field on the template page), FileField(enables remdering of a file field on the template) and 
    SubmitField(renders a submit button on the template)
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


class BlogForm(FlaskForm):
    """
    Forms for admin users to post blogs on the site
    The class inherits fromm the FlaskForm module which gives access to the TextArea(Renders a text field on the template)
    StringField(render an input field on the template page), FileField(enables remdering of a file field on the template) and 
    SubmitField(renders a submit button on the template)
    """
    blog_title = StringField('Blog Title', validators=[Required()],
                             render_kw={'placeholder': 'Blog Title'})
    blog_description = TextAreaField('Blog Body', validators=[Required()],
                                     render_kw={'rows': '25',
                                                'placeholder': "Use the '*' before you start the sentence to make a list", 'id': 'textbox'})
    picture = FileField('Blog Photo', validators=[
                        FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Submit')
