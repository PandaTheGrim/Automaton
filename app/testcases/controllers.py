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

from .models import TestCase, db
from app.testplans.models import TestPlan
from .forms import TestCaseCreateForm

module = Blueprint('testcases', __name__, url_prefix ='/automaton/cases')

def log_error(*args, **kwargs):
    current_app.logger.error(*args, **kwargs)

@module.before_request
def global_user_definition():
    g.user = current_user

@module.route('/')
@login_required
def list():
    return render_template('testcases/index.html')

@module.route('/create/testplanid/<int:testplanid>', methods=['GET', 'POST'])
@login_required
def create(testplanid):
    form = TestCaseCreateForm(request.form)
    cur_test_plan = TestPlan.query.filter_by(id = testplanid).first()
    status = 'None'
    try:
        if request.method == 'POST':
            if form.validate_on_submit():
                cur_test_case = TestCase.query.filter_by(name = request.form['name']).first()
                log_error(cur_test_plan)
                if cur_test_case is not None:
                    flash('Test case with that name already created. Please choose another name.', 'danger')
                    return render_template('testcases/create.html',
                                           testplanid=cur_test_plan.id,
                                           form = form)
                test_case = TestCase(name=request.form['name'],
                                     description=request.form['description'],
                                     status = status,
                                     testplan_id=cur_test_plan.id,
                                     user_id = g.user.id)
                db.session.add(test_case)
                db.session.commit()
                flash('Success testcase creation', 'success')
                return redirect(url_for('testplans.read', id=cur_test_plan.id))
            else:
                log_error('Validation error:\n\t'
                          'name: %s\n\t'
                          'description: %s',
                          request.form['name'], request.form['description'])
    except SQLAlchemyError as e:
        log_error('There was error while querying database', exc_info=e)
        db.session.rollback()
        flash('Something went wrong, please check your input data.', 'danger')
    request.form.get('testplanid')
    return render_template('testcases/create.html',
                           testplanid = cur_test_plan.id,
                           form = form)

@module.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    try:
        form = TestCaseCreateForm(request.form)
        cur_test_case = TestCase.query.filter_by(id = id).first()
        testplanid = cur_test_case.testplan_id
        cur_test_plan = TestPlan.query.filter_by(id = testplanid).first()
        if request.method == 'POST':
            cur_test_case.description = request.form['description']
            cur_test_case.comment = request.form['comment']
            db.session.commit()
            return redirect(url_for('testplans.read', id=cur_test_plan.id))
        return render_template('testcases/edit.html',
                               id = cur_test_case.id,
                               case = cur_test_case,
                               form = form)
    except SQLAlchemyError as e:
        log_error('There was error while querying database', exc_info=e)
        db.session.rollback()
        flash('Something went wrong, please check your input data.', 'danger')
        return redirect( url_for('dashboard.index') )

@module.route('/delete/<int:id>')
@login_required
def delete(id):
    try:
        cur_test_case = TestCase.query.filter_by(id = id).first()
        testplanid = cur_test_case.testplan_id
        cur_test_plan = TestPlan.query.filter_by(id = testplanid).first()
        db.session.delete(cur_test_case)
        db.session.commit()
        return redirect(url_for('testplans.read', id=cur_test_plan.id))
    except SQLAlchemyError as e:
        log_error('There was error while querying database', exc_info=e)
        db.session.rollback()
        flash('Something went wrong, please check your input data.', 'danger')
        return redirect( url_for('dashboard.index') )

@module.route('/passed/<int:id>')
@login_required
def passed(id):
    try:
        cur_test_case = TestCase.query.filter_by(id = id).first()
        cur_test_plan = TestPlan.query.filter_by(id = cur_test_case.testplan_id).first()
        if cur_test_plan.status != 'Closed':
            cur_test_case.status = 'Passed'
            db.session.commit()
            return redirect(url_for('testplans.read', id=cur_test_plan.id))
        else:
            flash('Sorry, but this test plan is already closed.', 'danger')
            return redirect(url_for('testplans.read', id=cur_test_plan.id))
    except SQLAlchemyError as e:
        log_error('There was error while querying database', exc_info=e)
        db.session.rollback()
        flash('Something went wrong, please check your input data.', 'danger')
        return redirect( url_for('dashboard.index') )


@module.route('/failed/<int:id>')
@login_required
def failed(id):
    try:
        cur_test_case = TestCase.query.filter_by(id = id).first()
        cur_test_plan = TestPlan.query.filter_by(id = cur_test_case.testplan_id).first()
        if cur_test_plan.status != 'Closed':
            cur_test_case.status = 'Failed'
            db.session.commit()
            return redirect(url_for('testplans.read', id=cur_test_plan.id))
        else:
            flash('Sorry, but this test plan is already closed.', 'danger')
            return redirect(url_for('testplans.read', id=cur_test_plan.id))
    except SQLAlchemyError as e:
        log_error('There was error while querying database', exc_info=e)
        db.session.rollback()
        flash('Something went wrong, please check your input data.', 'danger')
        return redirect( url_for('dashboard.index') )