from app.database import db


class TestPlan(db.Model):
    __tablename__ = 'test_plan'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(180), unique=False)
    comment = db.Column(db.String(300), unique=False)
    status = db.Column(db.String(20), unique=False)

    test_case = db.relationship("TestCase", backref="test_plan", lazy="dynamic")
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return '%r' % (self.name)
