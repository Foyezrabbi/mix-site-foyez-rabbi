"""
Admin utils function.
"""

import os
import imghdr
import secrets

from flask import current_app, request
from werkzeug.utils import secure_filename


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']


def save_picture(picture):
    picture = request.files['image']
    if picture and allowed_file(picture.filename):
        filename = secure_filename(picture.filename)
        _, extension = os.path.splitext(filename)
        random_hex = secrets.token_hex(8)
        picture_fn = random_hex + extension
        picture.save(os.path.join(current_app.config['UPLOAD_FOLDER_PATH'], picture_fn))
        return picture_fn
