from sqlalchemy import event

from app.database import db

class TestCase(db.Model):
    __tablename__ = 'test_case'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False)
    description = db.Column(db.String(80), unique=False)
    status = db.Column(db.String(80), unique=False)

    test_plan = db.relationship("TestPlan", backref="test_case", lazy="dynamic")
    user = db.relationship("User", backref="test_case", lazy="dynamic")

if __name__ == '__main__':
    # Make migration
    db.create_all()
    db.session.commit()