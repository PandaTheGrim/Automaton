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

from .models import TestPlan, db
from app.testcases.models import TestCase
from .forms import TestPlanCreateForm

module = Blueprint('testplans', __name__, url_prefix ='/automaton/testplans')

def log_error(*args, **kwargs):
    current_app.logger.error(*args, **kwargs)

@module.before_request
def global_user_definition():
    g.user = current_user

@module.route('/')
@login_required
def list():
    return render_template('testplans/index.html')

@module.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    form = TestPlanCreateForm(request.form)
    status = 'None'
    try:
        if request.method == 'POST':
            if form.validate_on_submit():
                cur_test_plan = TestPlan.query.filter_by(name = request.form['name']).first()
                if cur_test_plan is not None:
                    flash('Test plan with that name already created. Please choose another name.', 'danger')
                    return render_template('testplans/create.html',
                                           form = form)
                test_plan = TestPlan(name=request.form['name'],
                                     description=request.form['description'],
                                     status = status,
                                     user_id = g.user.id)
                db.session.add(test_plan)
                db.session.commit()
                id = test_plan.id
                log_error('id: %s', id)
                flash('Success release creation', 'success')
                return redirect(url_for('testplans.read', id=id))
            else:
                log_error('Validation error:\n\t'
                          'name: %s\n\t'
                          'description: %s\n\t'
                          'status: %s\n\t user.id: %s',
                          name, description, status, user.id)
    except SQLAlchemyError as e:
        log_error('There was error while querying database', exc_info=e)
        db.session.rollback()
        flash('Something went wrong, please check your input data.', 'danger')
    return render_template('testplans/create.html',
                       form = form)

@module.route('/view/<int:id>', methods=['GET', 'POST'])
@login_required
def read(id):
    cur_test_plan = TestPlan.query.filter_by(id = id).first()
    test_cases_array = TestCase.query.filter_by(testplan_id = id).all()
    return str(id)

@module.route('/edit')
@login_required
def update():
    pass

@module.route('/delete')
@login_required
def delete():
    pass
