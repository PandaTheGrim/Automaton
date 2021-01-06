from flask import (
    Blueprint,
    render_template,
    abort,
)

from flask_login import (login_required)

module = Blueprint('api', __name__, url_prefix='/api')


@module.route('/')
@login_required
def index():
    abort(418)


@module.route('/docs')
@login_required
def docs():
    return render_template('api/docs.html')
