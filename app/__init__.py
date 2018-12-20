# app/__init__.py

# third party imports

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap

# local imports

from instance.config import app_config

# initialize the db variable

db = SQLAlchemy()

login_manager = LoginManager()


def create_app(config_name):
    """
    create_app function that, given a configuration name, loads the correct configuration from the
    config.py file, as well as the configurations from the instance/config.py
    """

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_message = "You must be logged in to access this space"
    login_manager.login_view = "auth.login"
    migrate = Migrate(app, db)
    Bootstrap(app)

    from app import models

    from .admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix='/admin')

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .employer import employer as employer_blueprint
    app.register_blueprint(employer_blueprint)

    from .freelancer import freelancer as freelancer_blueprint
    app.register_blueprint(freelancer_blueprint)

    from .home import home as home_blueprint
    app.register_blueprint(home_blueprint)

    return app
