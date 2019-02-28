# app/employer/__init__.py
"""
This init file creates a blueprint for the employer routes of the application
"""

from flask import Blueprint

employer = Blueprint('employer', __name__)

from . import views
