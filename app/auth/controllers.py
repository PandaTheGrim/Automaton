import requests
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
from sqlalchemy.exc import SQLAlchemyError

from flask_login import (current_user, login_required, login_user, logout_user, confirm_login, fresh_login_required)

from app import login_manager

from .models import Users, db
from .forms import UserLoginForm, UserCreateForm

from .oauth import github

module = Blueprint('auth', __name__, url_prefix ='/account')

def log_error(*args, **kwargs):
    current_app.logger.error(*args, **kwargs)

@module.route('/login', methods=['GET', 'POST'])
def index():
    form = UserLoginForm(request.form)
    try:
        if request.method == 'POST' and form.validate_on_submit():
            username = request.form['username']
            password = request.form['password']
            cur_user = Users.query.filter_by(username = username).first()
            if cur_user is None:
                log_error('No user find with name %s', username)
                return render_template('auth/create.html',
                                       form = form)
            if cur_user.password == password:
                login_user(cur_user)
                return redirect(url_for('dashboard.index'))
            else:
                log_error('Password is incorrect %s', password)
    except SQLAlchemyError as e:
        log_error('There was error while querying database', exc_info=e)
        db.session.rollback()
        flash('Something went wrong, please check your input data.', 'danger')
    return render_template('auth/login.html',
                       form = form)

@module.route('/create', methods=['GET', 'POST'])
def create():
    form = UserCreateForm(request.form)
    try:
        if request.method == 'POST' and form.validate_on_submit():
            user = Users(username=request.form['username'],
                         email=request.form['email'],
                         password=request.form['password'])
            db.session.add(user)
            db.session.commit()
            flash('Success user creation', 'success')
            login_user(user)
            return redirect(url_for('dashboard.index'))
        else:
            return render_template('auth/create.html',
                                   form = form)
    except SQLAlchemyError as e:
        log_error('There was error while querying database', exc_info=e)
        db.session.rollback()
        flash('Something went wrong, please check your input data.', 'danger')
    return render_template('auth/create.html',
                           form = form)

@module.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return redirect(url_for('auth.index'))

@module.route('/profile', methods=['GET'])
def profile():
    try:
        user = Users.query.filter_by(username = current_user.username).first()
        return render_template('auth/profile.html',
                               user=user)
    except SQLAlchemyError as e:
        log_error('There was error while querying database', exc_info=e)
        db.session.rollback()
        flash('Something went wrong, please check your input data.', 'danger')
    return redirect( url_for('dashboard.index') )

client_id = github.client_id
redirect_uri = "http://127.0.0.1:5000/account/success_github"
params = {'client_id': client_id,
          'scope': 'user',
          'state': 'code123',
          'redirect_uri': redirect_uri,
          'allow_signup': "true"}

@module.route('/github_login', methods=['GET'])
def github_login():
    return redirect(github.get_authorize_url(**params))

@module.route('/success_github', methods=['GET'])
def sucess_github():
    if not request.args.get('code'):
        print("Please implement 403!!!")
    
    session = github.get_auth_session(data={'client_id': client_id,
                                            'client_secret': github.client_secret,
                                            'code': request.args.get('code'),
                                            'redirect_uri': redirect_uri,
                                            'state': 'code123'})

    resp = requests.get(
        github.base_url + "user", 
        headers={"Authorization": "token {}".format(session.access_token)}
    )

    github_user_json = resp.json()

    github_user_id = str(github_user_json["id"])
    username = github_user_json["login"]
    email = github_user_json["email"]

    user = Users.query.filter_by(github_id=github_user_id).first()

    if not user:
        user = Users(username=username,
                        email=email,
                        github_id=github_user_id)
        db.session.add(user)
        db.session.commit()

    login_user(user)
    return redirect(url_for('dashboard.index'))
