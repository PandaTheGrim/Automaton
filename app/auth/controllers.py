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
from sqlalchemy.exc import SQLAlchemyError

from .models import User, db
from .forms import UserLoginForm

module = Blueprint('auth', __name__, url_prefix ='/')


def log_error(*args, **kwargs):
    current_app.logger.error(*args, **kwargs)


@module.route('/', methods=['GET', 'POST'])
@module.route('/login', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        return redirect(url_for('dashboard.dashboard'))
    if request.method == 'GET':
        return render_template('auth/login.html')