from sqlalchemy import event

from app.database import db

class Release(db.Model):
    __tablename__ = 'release'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(180), unique=False)
    xml = db.Column(db.String(80), unique=False)
    status = db.Column(db.String(20), unique=False)

    user = db.relationship("User", backref="release", lazy="dynamic")