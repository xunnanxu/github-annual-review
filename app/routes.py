from app import app
import flask
from flask import Flask, request, render_template, send_from_directory
import requests
import json
import os
from datetime import date

from . import configs, github
from .reports import build_report

@app.route('/login')
def login():
    return flask.redirect('https://github.com/login/oauth/authorize?client_id=' + configs.CLIENT_ID +
        '&scope=repo read:user') 

@app.route('/oauth')
def complete_oauth():
    code = request.args.get('code')
    access_token = github.get_access_token(code)
    response = flask.redirect('/')
    response.set_cookie(configs.ACCESS_TOKEN_COOKIE, access_token)
    return response

@app.route('/')
def index():
    access_token = request.cookies.get(configs.ACCESS_TOKEN_COOKIE)
    if not access_token:
        return flask.redirect('/login')
    return render_template('index.html', time=date.today().strftime('%s'))

@app.route('/review')
def review():
    access_token = request.cookies.get(configs.ACCESS_TOKEN_COOKIE)
    if not access_token:
        return flask.abort(401)
    client = github.get_gh_client(access_token)
    report = build_report(client)
    return flask.jsonify(report)

@app.errorhandler(Exception)
def handle_error(e):
    return flask.jsonify({
            'code': e.code,
            'message': str(e),
    }), e.code