from flask import (
    g,
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

from sqlalchemy.exc import SQLAlchemyError

from .models import Release, db
from .forms import ReleaseCreateForm

module = Blueprint('releases', __name__, url_prefix ='/automaton/releases')

def log_error(*args, **kwargs):
    current_app.logger.error(*args, **kwargs)

@module.before_request
def global_user_definition():
    g.user = current_user

@module.route('/')
@login_required
def list():
    return render_template('releases/index.html')

@module.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    cur_release = None
    form = ReleaseCreateForm(request.form)
    xml = 'None to strore here.'
    status = 'In progress'
    try:
        if request.method == 'POST' and form.validate_on_submit():
            release = Release(name=request.form['name'],
                              description=request.form['description'],
                              xml = xml,
                              status = status,
                              user_id = g.user.id)
            id=release.id
            log_error('Dva')
            db.session.add(release)
            db.session.commit()
            flash('Success release creation', 'success')
            return redirect(url_for('releases.read', id=id))
        else:
            cur_release = Release.query.filter(Release.status == 'In progress').first()
            db.session.commit()
            if cur_release is not None:
                id = cur_release.id
                log_error('ALready have active release instance.\n\t id: %s\n\t name: %s', id, cur_release.name)
                flash('Please complete current release first!', 'warning')
                return redirect(url_for('releases.read', id=id))
    except SQLAlchemyError as e:
        log_error('There was error while querying database', exc_info=e)
        db.session.rollback()
        flash('Something went wrong, please check your input data.', 'danger')
    return render_template('releases/create.html',
                           form = form)

@module.route('/view/<id>')
@login_required
def read(id):
    abort(418)

@module.route('/edit')
@login_required
def update():
    pass

@module.route('/delete')
@login_required
def delete():
    pass
