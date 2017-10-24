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
from app.testplans.models import TestPlan
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
            db.session.add(release)
            db.session.commit(release)
            flash('Success release creation', 'success')
            return redirect(url_for('releases.read'))
        else:
            cur_release = Release.query.filter(Release.status == 'In progress').first()
            db.session.commit()
            if cur_release is not None:
                id = cur_release.id
                log_error('ALready have active release instance.\n\t id: %s\n\t name: %s', id, cur_release.name)
                flash('Please complete current release first!', 'warning')
                return redirect(url_for('releases.read'))
    except SQLAlchemyError as e:
        log_error('There was error while querying database', exc_info=e)
        db.session.rollback()
        flash('Something went wrong, please check your input data.', 'danger')
    return render_template('releases/create.html',
                           form = form)

@module.route('/current-release', methods=['GET', 'POST'])
@login_required
def read():
    cur_release = Release.query.filter(Release.status == 'In progress').first()
    test_plans = TestPlan.query.all()

    try:
        if request.method == 'POST':
            if g.user.id == cur_release.user_id:
                cur_release.status = 'Released'
                db.session.commit()
                flash('Release successfully closed! Congratulations!', 'success')
                return redirect(url_for('releases.history'))
            else:
                flash('You doesnt have permission to close this release. Only creator can do that action.', 'danger')
                return redirect(url_for('releases.read'))
    except SQLAlchemyError as e:
        log_error('There was error while querying database', exc_info=e)
        db.session.rollback()
        flash('Something went wrong, please check server logs for additional information.', 'danger')

    if cur_release != None:
        return render_template('releases/index.html', release=cur_release, test_plans=test_plans)
    else:
        flash('You dont have active releases. Please create it first!', 'danger')
        return redirect( url_for('releases.create'))

@module.route('/history')
@login_required
def history():
    old_releases = Release.query.filter(Release.status != 'In progress').all()
    if old_releases != None:
        return render_template('releases/history.html', releases=old_releases)
    else:
        flash('You dont have release history.', 'danger')
        return redirect( url_for('releases.read'))
