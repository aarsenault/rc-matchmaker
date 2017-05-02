
#  This is the database connection
# from app import db

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


# Create the user table
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<User {}>'.format(self.name)


# Create the table for histories



