# The application package. This contains the application data models
# and functions for sending emails.
#
# Modules:
#   emails - tools for sending emails from namebase asynchronously.
#   models - database models for the namebase application.
#
# Variables:
#   bootstrap (Bootstrap) - the bootstrap binder to the application.
#   mail (Mail) - the email sending binder to the application.
#   moment (Moment) - the moment.js to the application.
#   db (SQLAlchemy) - the binder to an ORM SQL database.
#   login_manager (LoginManager) - the login manager for the application.
#
# Functions:
#   create_app - configure and initialize the application.

from flask import Flask
from flask.ext.bootstrap import Bootstrap
from flask.ext.login import LoginManager
from flask.ext.mail import Mail
from flask.ext.moment import Moment
from flask.ext.sqlalchemy import SQLAlchemy

from config import config

# Binders or extensions to add functionality to the application.
bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.session_protection = 'strong'


def create_app(config_name):
    # Configure the application. Initialize the application. Attach
    # routes and custom error pages.
    #
    # Arguments:
    #   config_name (string) - the configuration for the application.
    #
    # Returns:
    #   (Flask) - the configured and initialized application.
    #
    # Raises:
    #   KeyError - when an invalid configuration name is provided.

    app = Flask(__name__)

    # Configure the application.
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # Initialize the application.
    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)

    # Attach routes and custom error pages.

    return app
