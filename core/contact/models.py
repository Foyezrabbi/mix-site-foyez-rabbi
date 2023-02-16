""" Contact app models """

from datetime import datetime

from .. import db
from ..utils import Updateable


class Contact(Updateable, db.Model):
    """Contact model"""

    __tablename__ = 'contact'

    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.Text, nullable=False)
    phone = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(80), nullable=False)
    subject = db.Column(db.String(80), nullable=False)
    fullname = db.Column(db.String(80), nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow())

    def __repr__(self):
        return f"Contact(id={self.id!r}, email={self.email!r}), phone={self.phone!r})"
