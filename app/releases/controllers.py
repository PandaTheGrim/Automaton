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

module = Blueprint('releases', __name__, url_prefix ='/automaton/releases')

@module.route('/')
def list():
    return render_template('releases/index.html')

@module.route('/create')
def create():
    pass

@module.route('/view')
def read():
    pass

@module.route('/edit')
def update():
    pass

@module.route('/delete')
def delete():
    pass
