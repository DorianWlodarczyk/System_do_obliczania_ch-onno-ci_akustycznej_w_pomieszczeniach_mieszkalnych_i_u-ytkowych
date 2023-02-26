from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func



class Norms(db.Model):
    pkey = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)

class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))


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
    reverb_time_120 = db.Column(db.Numeric(22,2), nullable=False)
    reverb_time_250 = db.Column(db.Numeric(22, 2), nullable=False)
    reverb_time_500 = db.Column(db.Numeric(22, 2), nullable=False)
    reverb_time_1000 = db.Column(db.Numeric(22, 2), nullable=False)
    reverb_time_2000 = db.Column(db.Numeric(22, 2), nullable=False)
    reverb_time_4000 = db.Column(db.Numeric(22, 2), nullable=False)

class NormsAbsorptionMultiplayer(db.Model):
    tablename = 'norms_absorption_multiplayer'
    norm_id = db.Column(db.Integer, db.ForeignKey('norms.id'), primary_key=True)
    absorption_multiplayer = db.Column(db.Numeric(22, 2), nullable=False)

class NormsReverbTimeNoReq(db.Model):
    tablename = 'norms_reverb_time_no_req'
    norm_id = db.Column(db.Integer, db.ForeignKey('norms.id'), primary_key=True)
    no_cubature_req = db.Column(db.Numeric(22, 2), nullable=False)

class NormsReverbTimeVolumeReq(db.Model):
    tablename = 'norms_reverb_time_volume_req'
    norm_id = db.Column(db.Integer, db.ForeignKey('norms.id'), primary_key=True)
    less_120 = db.Column(db.Numeric(22, 2), nullable=False)
    between_120_250 = db.Column(db.Numeric(22, 2), nullable=False)
    between_250_500 = db.Column(db.Numeric(22, 2), nullable=False)
    between_500_2000 = db.Column(db.Numeric(22, 2), nullable=False)
    more_2000 = db.Column(db.Numeric(22, 2), nullable=False)
    less_5000 = db.Column(db.Numeric(22, 2), nullable=False)
    more_5000 = db.Column(db.Numeric(22, 2), nullable=False)

class NormsReverbTimeHeightReq(db.Model):
    tablename = 'norms_reverb_time_height_req'
    norm_id = db.Column(db.Integer, db.ForeignKey('norms.id'), primary_key=True)
    h_less_4 = db.Column(db.Numeric(22, 2), nullable=False)
    h_between_4_16 = db.Column(db.Numeric(22, 2), nullable=False)
    h_more_16 = db.Column(db.Numeric(22, 2), nullable=False)

class NormsSpeechTransmissionIndex(db.Model):
    tablename = 'norms_speech_transmission_index'
    norm_id = db.Column(db.Integer, db.ForeignKey('norms.id'), primary_key=True)
    between_120_250 = db.Column(db.Numeric(22, 2), nullable=False)
    between_250_500 = db.Column(db.Numeric(22, 2), nullable=False)
    between_500_2000 = db.Column(db.Numeric(22, 2), nullable=False)
    more_2000 = db.Column(db.Numeric(22, 2), nullable=False)