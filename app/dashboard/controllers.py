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

from flask_login import (current_user, login_required, login_user, logout_user, confirm_login, fresh_login_required)

from sqlalchemy.exc import SQLAlchemyError

from app.testplans.models import TestPlan, db
from app.testcases.models import TestCase

module = Blueprint('dashboard', __name__, url_prefix ='/automaton')

@module.route('/index')
@login_required
def index():
    hash = {}
    case_array = []
    plans = TestPlan.query.all()
    # forming of testplan->testcases
    for plan in plans:
        cases = TestCase.query.filter_by(id = plan.id).all()
        for case in cases:
            case_array.append(case)
        hash[plan] = case_array
    print(hash)
    # percentage calculation
    metrics = {'status': 'current'}
    for key in hash:
        fail_counter = 0
        pass_counter = 0
        none_counter = 0
        metrics[key.name] = {}
        for value in hash[key]:
            if value.status == 'Passed':
                pass_counter += 1
            elif value.status == 'Failed':
                fail_counter += 1
            else:
                none_counter += 1
        metrics[key.name]['passed'] = pass_counter
        metrics[key.name]['failed'] = fail_counter
        metrics[key.name]['none'] = none_counter
    return render_template('dashboard/index.html', metrics=metrics)

