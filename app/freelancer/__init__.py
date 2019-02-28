# app/freelancer/__init__.py
"""
This init file creates a blueprint for the job seeker/freelancer routes of the application
"""

from flask import Blueprint

freelancer = Blueprint('freelancer', __name__)

from . import views
