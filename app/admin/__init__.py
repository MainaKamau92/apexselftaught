# app/admin/__init__.py
"""
This init file creates a blueprint for the admin routes of the application
"""


from flask import Blueprint

admin = Blueprint('admin', __name__)

from . import views
