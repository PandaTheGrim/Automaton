from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from app.releases.models import Release
from app.testplans.models import TestPlan
from app.testcases.models import TestCase

from .database import db

admin = Admin(name="Automaton", template_mode="bootstrap3")
admin.add_view(ModelView(Release, db.session))
admin.add_view(ModelView(TestPlan, db.session))
admin.add_view(ModelView(TestCase, db.session))
