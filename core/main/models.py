""" Main app models """


from datetime import datetime

from .. import db
from ..utils import Updateable


class Categories:
    DESIGN = 0x01
    DEV_WEB = 0x02
    FORMATION = 0x03
    DEV_MOBILE = 0x04
    DEV_LOGICIEL = 0x05


class Category(db.Model):
    """Project model"""

    __tablename__ = 'category'

    id = db.Column(db.Integer, primary_key=True)
    categories = db.Column(db.Integer)
    default = db.Column(db.Boolean, default=False, index=True)
    name = db.Column(db.String(30), unique=True, nullable=False)
    products = db.relationship('Project', backref='category', lazy='dynamic')

    def __init__(self, **kwagrs):
        super(Category, self).__init__(**kwagrs)
        if self.categories is None:
            self.categories = 0

    def __repr__(self):
        return f"Category(id={self.id!r}, timestamp={self.name!r})"

    def has_category(self, cat):
        return self.categories & cat == cat

    def add_category(self, cat):
        if not self.has_category(cat):
            self.categories += cat

    def remove_category(self, cat):
        if not self.has_category(cat):
            self.categories -= cat

    def reset_category(self):
        self.categories = 0

    @staticmethod
    def insert_category():
        categories = {
            'Création graphique': [Categories.DESIGN],
            'Développement Web': [Categories.DEV_WEB],
            'Coaching & Formation': [Categories.FORMATION],
            'Développement Mobile': [Categories.DEV_MOBILE],
            'Développement Logiciel': [Categories.DEV_MOBILE]
        }
        default_category = 'Développement Web'
        for c in categories:
            cat = Category.query.filter_by(name=c).first()
            if cat is None:
                cat = Category(name=c)
            cat.reset_category()
            for n in categories[c]:
                cat.add_category(n)
            cat.default = (cat.name == default_category)
            db.session.add(cat)
        db.session.commit()


class Project(Updateable, db.Model):
    """Project model"""

    __tablename__ = 'project'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    image = db.Column(db.String(80), nullable=False)
    timestamp = db.Column(
        db.DateTime,
        index=True, default=datetime.utcnow()
    )
    category_id = db.Column(
        db.Integer,
        db.ForeignKey('category.id'), nullable=False
    )
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id'), nullable=False
    )

    def __repr__(self):
        return f"Project(id={self.id!r}, timestamp={self.timestamp!r})"


class Storie(Updateable, db.Model):
    """Storie model"""

    __tablename__ = 'storie'
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(80), nullable=False)
    content = db.Column(db.Text)
    image = db.Column(db.String(80), nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow())
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id'), nullable=False
    )

    def __repr__(self):
        return f"Storie(id={self.id!r}, timestamp={self.timestamp!r})"


class Client(Updateable, db.Model):
    """Client model"""

    __tablename__ = 'partner'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    image = db.Column(db.String(80), nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow())
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id'), nullable=False
    )

    def __repr__(self):
        return f"Client(id={self.id!r}, timestamp={self.name!r})"
