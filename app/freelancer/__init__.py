# app/freelancer/__init__.py


from flask import Blueprint

freelancer = Blueprint('freelancer', __name__)

from . import views
