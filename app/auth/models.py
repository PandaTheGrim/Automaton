from sqlalchemy import event

from app.database import db
from app import login_manager


class Users(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(80), unique=False)
    email = db.Column(db.String(80), unique=True)
    github_id = db.Column(db.String(30), unique=True)

    role_id = db.Column(db.String, db.ForeignKey('roles.role'))
    role = db.relationship("Roles", backref="users")
    group_id = db.Column(db.String, db.ForeignKey('groups.group'))
    group = db.relationship("Groups", backref="users")
    test_plans = db.relationship("TestPlan", backref="users", lazy="dynamic")
    test_cases = db.relationship("TestCase", backref="users", lazy="dynamic")
    releases = db.relationship("Release", backref="users", lazy="dynamic")

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def is_admin(self):
        if str(self.role)[1:-1] == "admin":
            return True
        else:
            return False

    def get_id(self):
        return str(self.id)

    def get_username(self):
        return self.username

    def get_role(self):
        return str(self.role)[1:-1]

    def get_group(self):
        return self.group

    def __repr__(self):
        return '%r' % (self.username)

    def default_admin_user(app, db):
        try:
            admin = Users(username=app.config['ADMIN_USERNAME'],
                          password=app.config['ADMIN_PASSWORD'],
                          email=app.config['ADMIN_EMAIL'],
                          role=Roles.query.filter(Roles.role == "admin").first(),
                          group=Groups.query.filter(Groups.group == 'admin').first()
                          )
            db.session.add(admin)
            db.session.commit()
        except Exception as e:
            print('\nSome admin user addition error: ')
            print(e)
        return True


class Roles(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(80), unique=True)

    def __repr__(self):
        return '%r' % (self.role)

    def default_roles(app, db):
        default_roles = app.config['DEFAULT_ROLES']
        for item in default_roles:
            try:
                with db.session.begin_nested():
                    role = Roles(role=item)
                    db.session.add(role)
                db.session.commit()
            except:
                print('role ' + item + ' already exist')
        return True


class Groups(db.Model):
    __tablename__ = 'groups'

    id = db.Column(db.Integer, primary_key=True)
    group = db.Column(db.String(80), unique=True)

    def __repr__(self):
        return '%r' % (self.group)

    def default_groups(app, db):
        default_groups = app.config['DEFAULT_GROUPS']
        for item in default_groups:
            try:
                with db.session.begin_nested():
                    group = Groups(group=item)
                    db.session.add(group)
                db.session.commit()
            except:
                print('Group ' + item + ' already exist')
        return True


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))