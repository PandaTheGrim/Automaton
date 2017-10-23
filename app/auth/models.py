from sqlalchemy import event

from app.database import db

class Users(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(80), unique=False)
    email = db.Column(db.String(80), unique=True)
    role = db.Column(db.String(7),unique=False, default= 'users')

    test_plans = db.relationship("TestPlan", backref="users", lazy="dynamic")
    test_cases = db.relationship("TestCase", backref="users", lazy="dynamic")
    releases = db.relationship("Release", backref="users", lazy="dynamic")