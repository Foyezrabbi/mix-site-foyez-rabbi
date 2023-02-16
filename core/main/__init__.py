"""
Main app page routes.
"""

from flask import Blueprint

main = Blueprint("main", __name__)

from . import routes
