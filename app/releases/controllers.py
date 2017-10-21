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
    abort(418)

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


'''
<li class="nav-item" data-toggle="tooltip" data-placement="right" title="Tables">
          <a class="nav-link" href="{{ url_for('releases.list') }}">
            <i class="fa fa-fw fa-table"></i>
            <span class="nav-link-text">Test-plans</span>
          </a>'''
