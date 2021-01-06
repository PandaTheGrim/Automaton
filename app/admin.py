from flask import (
    abort,
    current_app
)
from flask_admin import Admin, expose, AdminIndexView
from flask_admin.contrib import sqla, fileadmin
from flask_login import current_user

from app.auth.models import Users, Roles, Groups
from app.releases.models import Release
from app.testcases.models import TestCase
from app.testplans.models import TestPlan
from .database import db


def log_error(*args, **kwargs):
    current_app.logger.error(*args, **kwargs)


class ModelView(sqla.ModelView):
    def is_accessible(self):
        if not current_user.is_active or not current_user.is_authenticated:
            log_error('Anonymous admin panel load attempt at ModelView')
            abort(403)

        if current_user.is_admin():
            return True

        log_error('User %s admin panel load attempt at ModelView', current_user.get_username())
        abort(403)


class FileAdmin(fileadmin.FileAdmin):
    def is_accessible(self):
        if not current_user.is_active or not current_user.is_authenticated:
            log_error('Anonymous admin panel load attempt at FileAdmin')
            return False

        if current_user.is_admin():
            return True

        log_error('User %s admin panel load attempt at FileAdmin', current_user.get_username())
        return False

    @expose('/old_index')
    @expose('/old_b/<path:path>')
    def index(self, path=None):
        if not is_accessible(self):
            abort(403)

    @expose('/')
    @expose('/b/<path:path>')
    def index_view(self, path=None):
        if not is_accessible(self):
            abort(403)

    @expose('/upload/', methods=('GET', 'POST'))
    @expose('/upload/<path:path>', methods=('GET', 'POST'))
    def upload(self, path=None):
        if not is_accessible(self):
            abort(403)

    @expose('/download/<path:path>')
    def download(self, path=None):
        if not is_accessible(self):
            abort(403)

    @expose('/mkdir/', methods=('GET', 'POST'))
    @expose('/mkdir/<path:path>', methods=('GET', 'POST'))
    def mkdir(self, path=None):
        if not is_accessible(self):
            abort(403)

    @expose('/delete/', methods=('POST',))
    def delete(self):
        if not is_accessible(self):
            abort(403)

    @expose('/rename/', methods=('GET', 'POST'))
    def rename(self):
        if not is_accessible(self):
            abort(403)

    @expose('/edit/', methods=('GET', 'POST'))
    def edit(self):
        if not is_accessible(self):
            abort(403)

    @expose('/action/', methods=('POST',))
    def action_view(self):
        if not is_accessible(self):
            abort(403)


class IndexView(AdminIndexView):
    @expose('/')
    def index(self):
        if not current_user.is_active or not current_user.is_authenticated:
            log_error('Anonymous admin panel load attempt at AdminIndexView')
            abort(403)

        if not current_user.is_admin():
            log_error('User %s admin panel load attempt at AdminIndexView',
                      current_user.get_username())
            abort(403)

        arg1 = 'Hello admin!'
        return self.render('admin/master.html', arg1=arg1)


admin = Admin(name="Automaton", template_mode="bootstrap3", index_view=IndexView(name='Home'))
admin.add_view(ModelView(Roles, db.session))
admin.add_view(ModelView(Groups, db.session))
admin.add_view(ModelView(Users, db.session))
admin.add_view(ModelView(Release, db.session))
admin.add_view(ModelView(TestPlan, db.session))
admin.add_view(ModelView(TestCase, db.session))
