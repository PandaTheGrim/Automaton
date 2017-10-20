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

module = Blueprint('cases', __name__, url_prefix ='/automaton/cases')

@module.route('/')
def list():
    pass

@module.route('/create')
def create():
    pass

@module.route('/view')
def read():
    pass

@module.route('/edit')
def update():
    pass

@module.route('/edit')
def delete():
    pass