from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Patient(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    patient_name = db.Column(db.String(128))
    allergy = db.Column(db.String(128))
    contact = db.Column(db.String(128))
    meds = db.Column(db.String(128))
    date = db.Column(db.DateTime(timezone = True), default = func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    added_by = db.Column(db.String(128))
    is_emergency = db.Column(db.Boolean)
    additional_notes = db.Column(db.String(1024))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(128), unique = True)
    password = db.Column(db.String(128))
    first_name = db.Column(db.String(128))
    patients = db.relationship('Patient')    