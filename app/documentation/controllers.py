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

module = Blueprint('docs', __name__, url_prefix ='/docs')

@module.route('/')
@login_required
def index():
    return render_template('documentation/index.html')

@module.route('/releases')
@login_required
def releases():
    return render_template('documentation/releases.html')

@module.route('/testplans')
@login_required
def testplans():
    return render_template('documentation/testplans.html')

@module.route('/testcases')
@login_required
def testcases():
    return render_template('documentation/testcases.html')

@module.route('/metrics')
@login_required
def metrics():
    return render_template('documentation/metrics.html')

@module.route('/admin')
@login_required
def admin():
    return render_template('documentation/admin.html')

@module.route('/roles')
@login_required
def roles():
    return render_template('documentation/roles.html')

@module.route('/groups')
@login_required
def groups():
    return render_template('documentation/groups.html')