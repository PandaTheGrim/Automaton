import requests
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

from .models import User, db
from .forms import UserLoginForm

from .oauth import github

module = Blueprint('auth', __name__, url_prefix ='/')


def log_error(*args, **kwargs):
    current_app.logger.error(*args, **kwargs)


@module.route('/', methods=['GET', 'POST'])
@module.route('login', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        return redirect(url_for('dashboard.index'))
    if request.method == 'GET':
        return render_template('auth/login.html')

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
