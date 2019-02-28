# app/auth/__init__.py

"""
This init file creates a blueprint for the authentication routes of the application
"""
from flask import Blueprint

auth = Blueprint('auth', __name__)

from . import views
