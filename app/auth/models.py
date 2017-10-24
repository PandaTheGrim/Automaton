from sqlalchemy import event

from app.database import db
from app import login_manager

class Users(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(80), unique=False)
    email = db.Column(db.String(80), unique=True)
    role = db.Column(db.String(7),unique=False, default= 'user')

    test_plans = db.relationship("TestPlan", backref="users", lazy="dynamic")
    test_cases = db.relationship("TestCase", backref="users", lazy="dynamic")
    releases = db.relationship("Release", backref="users", lazy="dynamic")

    github_id = db.Column(db.String(30), unique=True)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))