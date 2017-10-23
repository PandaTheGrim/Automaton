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
        if request.method == 'POST' and form.validate():
            username = request.form['username']
            password = request.form['password']
            current_user = Users.query.filter_by(username = username).first()
            if current_user is None:
                log_error('No user find with name %s', username)
                return render_template('auth/create.html',
                                       form = form)
            if current_user.password == password:
                g.user = current_user.id
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
        if request.method == 'POST' and form.validate():
            user = Users(username=request.form['username'],
                         email=request.form['email'],
                         password=request.form['password'])
            g.user = user.id
            db.session.add(user)
            db.session.commit()
            flash('Success user creation', 'success')
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



client_id = github.client_id
redirect_uri = "http://127.0.0.1:5000/success_github"
params = {'client_id': client_id,
          'scope': 'user',
          'state': 'code123',
          'redirect_uri': redirect_uri,
          'allow_signup': "true"}

url = github.get_authorize_url(**params)

@module.route('github_login', methods=['GET'])
def github_login():
    return redirect(url)

@module.route('success_github', methods=['GET'])
def sucess_github():
    if request.args.get('code'):
        session = github.get_auth_session(data={'client_id': client_id,
                                                'client_secret': github.client_secret,
                                                'code': request.args.get('code'),
                                                'redirect_uri': redirect_uri,
                                                'state': 'code123'})

        #TODO
        '''
        after implementation of basic auth, we need to check if user no anonymous,
        if user have account in system we need to login it, and else we need to create new user with
        credentials from api.github 
        '''

        return redirect('/')
