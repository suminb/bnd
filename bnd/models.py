from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID, JSON
from __init__ import app

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    oauth_id = db.Column(db.String, unique=True)
    given_name = db.Column(db.String)
    family_name = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    data = db.Column(JSON)


class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)


class UserTeamAssoc(db.Model):
    id = db.Column(db.Integer, primary_key=True)


class Goal(db.Model):
    id = db.Column(db.Integer, primary_key=True)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)

