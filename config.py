"""
Flask app configuration.
Set Flask configuration from environment variables
"""

import datetime
from os import mkdir, urandom, environ, path
from werkzeug.utils import secure_filename


BASE_DIR = path.abspath(path.dirname(__file__))


class Config:

    DEBUG = False
    TESTING = False
    DEVELOPMENT = False

    SITE_NAME = environ.get("SITE_NAME")
    SQLALCHEMY_ECHO = False
    SECRET_KEY = environ.get('SECRET_KEY', urandom(24))
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PHONE_NUMBER = environ.get("PHONE_NUMBER")
    PHONE_NUMBER_TWO = environ.get("PHONE_NUMBER_TWO")
    MAIL_SERVER = environ.get('MAIL_SERVER')
    FLASKY_ADMIN = environ.get('FLASKY_ADMIN')
    MAIL_POST = int(environ.get('MAIL_POST', '587'))
    MAIL_USE_TLS = environ.get('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']

    MAIL_SENDER = environ.get('MAIL_SENDER')
    EMAIL_ADDRESS = environ.get('FLASKY_ADMIN')
    MAIL_USERNAME = environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = environ.get('MAIL_PASSWORD')
    MAIL_SUBJECT_PREFIX = environ.get("MAIL_SUBJECT")

    MAX_CONTENT_LENGTH = 16 * 1000 * 1000
    ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg']
    UPLOAD_FOLDER_PATH = path.join(BASE_DIR, 'upload/')

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    DEVELOPMENT = True
    SQLALCHEMY_DATABASE_URI = environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + path.join(BASE_DIR, 'dev.sqlite3')


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = environ.get('DATABASE_URL') or \
        'sqlite:///' + path.join(BASE_DIR, 'prod.sqlite3')

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)

        import logging
        from logging.handlers import SMTPHandler

        credentials = None
        secure = None

        if getattr(cls, 'MAIL_USERNAME', None) is not None:
            credentials = (cls.MAIL_USERNAME, cls.MAIL_PASSWORD)
            if getattr(cls, 'MAIL_USE_TLS', None):
                secure = ()

        mail_handler = SMTPHandler(
            mailhost=(cls.MAIL_SERVER, cls.MAIL_PORT),
            fromaddr=cls.MAIL_SENDER,
            toaddrs=[cls.FLASKY_ADMIN],
            subject=cls.MAIL_SUBJECT_PREFIX + ' Application Error',
            credentials=credentials,
            secure=secure
        )
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)


config = {
    'prod': ProductionConfig,
    'dev': DevelopmentConfig,
}
