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

module = Blueprint('dashboard', __name__, url_prefix ='/')

@module.route('/')
def dashboard():
    return render_template('dashboard/index.html')