import requests
from github import Github

from .. import configs

def get_access_token(code):
    payload = {
        'client_id': configs.CLIENT_ID,
        'client_secret': configs.CLIENT_SECRET,
        'code': code
    }
    headers = {'Accept': 'application/json'}
    r = requests.post('https://github.com/login/oauth/access_token', data=payload, headers=headers)
    resp = r.json()
    return resp['access_token']

def get_gh_client(access_token):
    return Github(access_token)