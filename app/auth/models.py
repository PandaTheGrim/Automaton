from sqlalchemy import event

from app.database import db

class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(80), unique=False)
    email = db.Column(db.String(80), unique=True)
    role = db.Column(db.String(7),unique=False, default= 'user')

    comment = db.relationship("Post", backref="user", lazy="dynamic")

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)