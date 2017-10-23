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