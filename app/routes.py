from app import app
import flask
from flask import Flask, redirect, request, render_template, send_from_directory
import requests
import json
import os
from datetime import datetime

from . import configs, github
from .github import get_gh_client
from .reports import build_report

@app.route('/login')
def login():
    return redirect('https://github.com/login/oauth/authorize?client_id=' + configs.CLIENT_ID +
        '&scope=repo read:user') 

@app.route('/')
def index():
    return render_template('index.html', user='abc', time=datetime.now().strftime('%s'))

@app.route('/review')
def review():
    access_token = request.cookies.get(configs.ACCESS_TOKEN_COOKIE)
    client = None
    if access_token:
        client, access_token = get_gh_client(access_token=access_token)
    else:
        code = request.args.get('code')
        if not code:
            return redirect('/login')
        client, access_token = get_gh_client(code=code)
    app.logger.info(access_token)

    report = build_report(client)

    resp = flask.jsonify(report)
    resp.set_cookie(configs.ACCESS_TOKEN_COOKIE, access_token)
    return resp
