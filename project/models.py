from flask_login import UserMixin

from . import db


class User(UserMixin, db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(255))
    dn = db.Column(db.String(255), unique=True)