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

module = Blueprint('api', __name__, url_prefix ='/api')

@module.route('/')
@login_required
def index():
    abort(418)

@module.route('/docs')
@login_required
def docs():
    return render_template('api/docs.html')