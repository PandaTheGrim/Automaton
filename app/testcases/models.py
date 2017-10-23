from sqlalchemy import event

from app.database import db

class TestCase(db.Model):
    __tablename__ = 'test_case'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False)
    description = db.Column(db.String(180), unique=False)
    status = db.Column(db.String(20), unique=False)

    test_plan_id = db.Column(db.Integer(), db.ForeignKey('test_plan.id'))
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'))