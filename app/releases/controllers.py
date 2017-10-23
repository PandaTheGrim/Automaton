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

from .models import Release, db
from .forms import ReleaseCreateForm

module = Blueprint('releases', __name__, url_prefix ='/automaton/releases')

def log_error(*args, **kwargs):
    current_app.logger.error(*args, **kwargs)

@module.route('/')
def list():
    return render_template('releases/index.html')

@module.route('/create', methods=['GET', 'POST'])
def create():
    cur_release = Release.query.filter_by(status='In progress').first()
    if cur_release is not None:
        flash('Please complete current release first!', 'warning')
        return redirect(url_for('release.view', id=cur_release.id))
    form = ReleaseCreateForm(request.form)
    try:
        if request.method == 'POST' and form.validate():
            release = Release(**form.data)
            release.xml = 'None to store here'
            release.status = 'In progress'
            release.user = g.user
            id = release.id
            db.session.add(release)
            db.session.commit()
            flash('Success release creation', 'success')
            return redirect(url_for('release.view', id=id))
    except SQLAlchemyError as e:
        log_error('There was error while querying database', exc_info=e)
        db.session.rollback()
        flash('Something went wrong, please check your input data.', 'danger')
    return render_template('releases/create.html')

@module.route('/view/<int:id>')
def read(id):
    pass

@module.route('/edit')
def update():
    pass

@module.route('/delete')
def delete():
    pass
