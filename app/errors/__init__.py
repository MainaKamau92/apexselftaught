# app/freelancer/__init__.py


from flask import Blueprint

error = Blueprint('error', __name__)

from . import views
