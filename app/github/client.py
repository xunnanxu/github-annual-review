import requests
from github import Github

from .. import configs

def get_gh_client(code=None, access_token=None):
    if code:
        payload = {
            'client_id': configs.CLIENT_ID,
            'client_secret': configs.CLIENT_SECRET,
            'code': code
        }
        headers = {'Accept': 'application/json'}
        r = requests.post('https://github.com/login/oauth/access_token', data=payload, headers=headers)
        resp = r.json()
        access_token = resp['access_token']
    return Github(access_token), access_token