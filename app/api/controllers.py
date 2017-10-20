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

module = Blueprint('api', __name__, url_prefix ='/api')

@module.route('/')
def index():
    return 'Hello world!'