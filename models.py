from flask_login import UserMixin
from app import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(100))
    role = db.Column(db.String(100))

class availableform(db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    startdate = db.Column(db.Date)
    enddate = db.Column(db.Date)
    avail_hours = db.Column(db.String(10))
    interest = db.Column(db.String(200))
    involvement = db.Column(db.String(100))
    typeofwork = db.Column(db.String(100))

class timeentryform(db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    startdate = db.Column(db.Date)
    enddate = db.Column(db.Date)
    hours_spent = db.Column(db.String(10))
    involvement = db.Column(db.String(100))
    typeofwork = db.Column(db.String(100))
    project = db.Column(db.String(100))
    owner = db.Column(db.String(100))