# app/employer/__init__.py

from flask import Blueprint

employer = Blueprint('employer', __name__)

from . import views
