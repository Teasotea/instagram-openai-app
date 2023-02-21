from flask_login import UserMixin
from . import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))

    email_verified = db.Column(db.Boolean, default=False)
    registered_on = db.Column(db.DateTime, nullable=False)
    instagram_key = db.Column(db.String(100), unique=True)
    instagram_username = db.Column(db.String(100), unique=True)