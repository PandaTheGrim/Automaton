import os
from rauth import OAuth2Service

OAUTH_CREDENTIALS = {
    'github': {
        'id': os.environ.get('GITHUB_CLIENT_ID', 'ID'),
        'secret': os.environ.get('GITHUB_CLIENT_SECRET', 'SECRET')
    },
}

github = OAuth2Service(
    name='github',
    base_url='https://api.github.com/',
    authorize_url='https://github.com/login/oauth/authorize',
    access_token_url='https://github.com/login/oauth/access_token',
    client_id=OAUTH_CREDENTIALS['github']['id'],
    client_secret=OAUTH_CREDENTIALS['github']['secret']
)
