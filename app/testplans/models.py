from sqlalchemy import event

from app.database import db

class TestPlan(db.Model):
    __tablename__ = 'test_plan'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(80), unique=False)
    status = db.Column(db.String(80), unique=False)

    test_case = db.relationship("TestCase", backref="test_plan", lazy="dynamic")
    user = db.relationship("User", backref="test_plan", lazy="dynamic")

if __name__ == '__main__':
    # Make migration
    db.create_all()
    db.session.commit()