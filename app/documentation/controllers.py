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

module = Blueprint('docs', __name__, url_prefix ='/docs')

@module.route('/')
def index():
    return render_template('documentation/index.html')