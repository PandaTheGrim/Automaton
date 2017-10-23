from flask import (
    Blueprint,
    render_template,
    request,
    flash,
    abort,
    redirect,
    url_for,
    current_app,
)

from flask_login import (current_user, login_required, login_user, logout_user, confirm_login, fresh_login_required)

module = Blueprint('cases', __name__, url_prefix ='/automaton/cases')

@module.route('/')
@login_required
def list():
    return render_template('testcases/index.html')

@module.route('/create')
@login_required
def create():
    pass

@module.route('/view')
@login_required
def read():
    pass

@module.route('/edit')
@login_required
def update():
    pass

@module.route('/edit')
@login_required
def delete():
    pass