from flask import (
    Blueprint,
    render_template,
)
from flask_login import (login_required)

from app.testcases.models import TestCase
from app.testplans.models import TestPlan

module = Blueprint('dashboard', __name__, url_prefix='/automaton')


@module.route('/index')
@login_required
def index():
    hash = {}
    plans = TestPlan.query.all()
    # forming of testplan->testcases
    for plan in plans:
        case_array = []
        cases = TestCase.query.filter_by(id=plan.id).all()
        for case in cases:
            case_array.append(case)
        hash[plan] = case_array
    print(hash)
    # percentage calculation
    metrics = {}
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
