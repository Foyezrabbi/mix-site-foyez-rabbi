"""
Admin app page routes.
"""

from flask import Blueprint

admin = Blueprint("admin", __name__, url_prefix='/21fh08/')

from . import routes
