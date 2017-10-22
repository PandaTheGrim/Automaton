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

module = Blueprint('plans', __name__, url_prefix ='/automaton/plans')

@module.route('/')
def list():
    return render_template('testplans/index.html')

@module.route('/create')
def create():
    return render_template('testplans/create.html')

@module.route('/view')
def read():
    pass

@module.route('/edit')
def update():
    pass

@module.route('/edit')
def delete():
    pass
