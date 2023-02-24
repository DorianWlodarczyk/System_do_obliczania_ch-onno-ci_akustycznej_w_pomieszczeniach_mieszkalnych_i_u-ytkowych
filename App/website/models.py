from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func




class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    notes = db.relationship('Notes')


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

class Projects(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(255), unique=True, nullable=False)
    norm_id = db.Column(db.Integer, nullable=False)
    up_to_norm = db.Column(db.String(3), nullable=False)
    length = db.Column(db.Numeric(22,2), nullable=False)
    width = db.Column(db.Numeric(22,2), nullable=False)
    height = db.Column(db.Numeric(22,2), nullable=False)
    floor = db.Column(db.Numeric(22,2), nullable=False)
    sufit_id = db.Column(db.Integer, nullable=False)
    wall1_id = db.Column(db.Integer, nullable=False)
    wall2_id = db.Column(db.Integer, nullable=False)
    wall3_id = db.Column(db.Integer, nullable=False)
    wall4_id = db.Column(db.Integer, nullable=False)
    furniture = db.Column(db.Text, nullable=False)
    _120 = db.Column(db.Numeric(22,2), nullable=False)
    _250 = db.Column(db.Numeric(22,2), nullable=False)
    _500 = db.Column(db.Numeric(22,2), nullable=False)
    _1000 = db.Column(db.Numeric(22,2), nullable=False)
    _2000 = db.Column(db.Numeric(22,2), nullable=False)
    _4000 = db.Column(db.Numeric(22,2), nullable=False)