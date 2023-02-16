"""
Initialize app
"""

import os
import logging
from logging.handlers import TimedRotatingFileHandler

from flask import Flask, current_app, render_template

from flask_mail import Mail
from flask_moment import Moment
from flask_bcrypt import Bcrypt
from flask_ckeditor import CKEditor
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

from config import config


mail = Mail()
db = SQLAlchemy()
moment = Moment()
bcrypt = Bcrypt()
ckeditor = CKEditor()
login_manager = LoginManager()

login_manager.login_view = 'admin.loginPage'
login_manager.session_protection = "strong"
login_manager.login_message_category = 'info'
login_manager.needs_refresh_message_category = 'danger'


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    mail.init_app(app)
    moment.init_app(app)
    bcrypt.init_app(app)
    ckeditor.init_app(app)
    login_manager.init_app(app)

    db.init_app(app)

    with app.app_context():

        from .main import main as main_blueprint
        app.register_blueprint(main_blueprint)

        from .admin import admin as admin_blueprint
        app.register_blueprint(admin_blueprint)

        @app.errorhandler(404)
        def pageNotFound(error):
            page_title = f"{error.code} - page not found !"
            return render_template(
                'page/error.html',
                page_title=page_title,
                error=error
            ), 404

        @app.errorhandler(500)
        def internalServerError(error):
            page_title = f"{error.code} - few things went wrong"
            return render_template(
                'page/error.html',
                page_title=page_title,
                error=error
            ), 500

        @app.errorhandler(400)
        def keyError(error):
            page_title = f"{error.code} - invalid request resulted in KeyError."
            return render_template(
                'page/error.html',
                page_title=page_title,
                error=error
            ), 400

        @app.before_request
        def log_entry():
            app.logger.debug("Processing request")


        @app.context_processor
        def context_processor():
            from .admin.routes import categories, projects, clients, stories
            return dict(
                categories=categories, projects=projects,
                clients=clients, stories=stories
            )

        @app.teardown_request
        def log_exit(exc):
            app.logger.debug("Application processing completed", exc_info=exc)

        try:
            if not os.path.exists('upload'):
                os.mkdir('upload')
        except OSError:
            pass

        if not app.debug:
            if not os.path.exists('logs'):
                os.mkdir('logs')
            file_handler = TimedRotatingFileHandler('logs/logging.log', when="D", backupCount=7)
            file_handler.setFormatter(logging.Formatter(
                '''Time: %(asctime)s
                Level: %(levelname)s
                Method: %(message)s
                Path: %(url)s
                IP: %(ip)s
                User ID: %(user_id)s
                Message: %(message)s
                -----------------------'''))

            file_handler.setLevel(logging.ERROR)
            file_handler.setLevel(logging.INFO)
            app.logger.addHandler(file_handler)
            app.logger.info('running app')

        return app
