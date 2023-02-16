"""
Admin Models
"""

import hashlib
from time import time
from datetime import datetime

from flask_login import UserMixin, AnonymousUserMixin
from flask import current_app, redirect, flash, url_for, request
from werkzeug.security import generate_password_hash, check_password_hash

import jwt
from . import admin
from ..utils import Updateable
from .. import db, login_manager
from core.main.models import Project, Client, Storie


class Permission:
    ADMIN = 0x05
    MODERATE = 0x07


class Role(db.Model):

    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    permissions = db.Column(db.Integer)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __init__(self, **kwagrs):
        super(Role, self).__init__(**kwagrs)
        if self.permissions is None:
            self.permissions = 0

    def __repr__(self):
        return f"Role(id={self.id!r}, name={self.name!r}, users={self.users!r})"

    def has_permission(self, perm):
        return self.permissions & perm == perm

    def add_permission(self, perm):
        if not self.has_permission(perm):
            self.permissions += perm

    def remove_permission(self, perm):
        if not self.has_permission(perm):
            self.permissions -= perm

    def reset_permission(self):
        self.permissions = 0

    @staticmethod
    def insert_roles():
        roles = {
            'Moderateur': [Permission.MODERATE],
            'Administrateur': [Permission.ADMIN]
        }
        default_role = 'Administrateur'
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.reset_permission()
            for perm in roles[r]:
                role.add_permission(perm)
            role.default = (role.name == default_role)
            db.session.add(role)
        db.session.commit()


class User(Updateable, UserMixin, db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(
        db.String(80), unique=True,
        nullable=False
    )
    password = db.Column(
        db.String(200), nullable=False,
        unique=False, primary_key=False
    )
    joined_at = db.Column(
        db.DateTime, nullable=False,
        default=datetime.utcnow()
    )
    last_seen = db.Column(db.DateTime, default=datetime.utcnow())
    role_id = db.Column(
        db.Integer, db.ForeignKey('roles.id'),
        nullable=True
    )
    projects = db.relationship(
        'Project',
        backref='user',
        lazy='dynamic'
    )
    clients = db.relationship(
        'Client',
        backref='user',
        lazy='dynamic'
    )
    stories = db.relationship(
        'Storie',
        backref='user',
        lazy='dynamic'
    )

    def __init__(self, **kwagrs):
        super(User, self).__init__(**kwagrs)
        if self.role is None:
            if self.email == current_app.config['FLASKY_ADMIN']:
                self.role = Role.query.filter_by(name='Administrateur').first()
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()

    def __repr__(self):
        return f"User(id={self.id!r}, email={self.email!r}"

    def can(self, perm):
        return self.role is not None and self.role.has_permission(perm)

    def is_admin(self):
        return self.can(Permission.ADMIN)

    def ping(self):
        self.last_seen = datetime.utcnow()
        db.session.add(self)
        db.session.commit()

    def change_email(self):
        self.image_file = self.gravatar_hash()
        db.session.add(self)
        return True

    def gravatar_hash(self):
        return hashlib.md5(self.email.lower().encode('utf-8')).hexdigest()

    def gravatar(self, size=256, default='identicon', rating='g'):
        if request.is_secure:
            url = 'https://secure.gravatar.com/avatar'
        else:
            url = 'http://www.gravatar.com/avatar'
            hasher = self.gravatar_hash()
        return f"{url}/{hasher}?s={size}&d={default}&r={rating}"

    @property
    def password_hash(self):
        return AttributeError("Le mot de passe n'est pas un attribut lisible")

    @password_hash.setter
    def password_hash(self, password):
        self.password = generate_password_hash(password_hash)

    def verify_password(self, password):
        return check_password_hash(self.password, password)

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'admin.resetPasswordPage': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'], algorithm='HS256'
        )

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(
                token, current_app.config['SECRET_KEY'],
                algorithms=['HS256'])['auth.resetPasswordPage']
        except:
            return
        return User.query.get(id)


class AnonymousUser(AnonymousUserMixin):

    def can(self, permissions):
        return False

    def is_admin(self):
        return False


login_manager.anonymous_user = AnonymousUser


@login_manager.user_loader
def load_user(user_id):
    if user_id is not None:
        return User.query.get(int(user_id))
    return None
