from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    notes = db.relationship('Note')


class Material(db.Model):
    __tablename__ = 'materials'
    pkey = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    _120 = db.Column(db.Numeric(precision=22, scale=2), nullable=False)
    _250 = db.Column(db.Numeric(precision=22, scale=2), nullable=False)
    _500 = db.Column(db.Numeric(precision=22, scale=2), nullable=False)
    _1000 = db.Column(db.Numeric(precision=22, scale=2), nullable=False)
    _2000 = db.Column(db.Numeric(precision=22, scale=2), nullable=False)
    _4000 = db.Column(db.Numeric(precision=22, scale=2), nullable=False)

class Norms(db.Model):
    #__tablename__ = 'norms'
    pkey = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    absorption_multiplayer = db.Column(db.Numeric(22,2), nullable=False)