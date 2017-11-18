#from flask import current_user
from flask_admin import Admin, BaseView
from flask_admin.contrib.sqla import ModelView

from app.auth.models import Users, Roles, Groups
from app.releases.models import Release
from app.testplans.models import TestPlan
from app.testcases.models import TestCase

from .database import db

admin = Admin(name="Automaton", template_mode="bootstrap3")
admin.add_view(ModelView(Roles, db.session))
admin.add_view(ModelView(Groups, db.session))
admin.add_view(ModelView(Users, db.session))
admin.add_view(ModelView(Release, db.session))
admin.add_view(ModelView(TestPlan, db.session))
admin.add_view(ModelView(TestCase, db.session))


class MyView(BaseView):
    def is_accessible(current_user):
        return current_user.is_admin()
