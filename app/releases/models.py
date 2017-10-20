from sqlalchemy import event

from app.database import db

class Release(db.Model):
    __tablename__ = 'release'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    xml = db.Column(db.String(80), unique=False)
    status = db.Column(db.String(80), unique=False)

    test_plan = db.relationship("TestPlan", backref="release", lazy="dynamic")
    user = db.relationship("User", backref="release", lazy="dynamic")

if __name__ == '__main__':
    # Make migration
    db.create_all()
    db.session.commit()