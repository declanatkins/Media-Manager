from functools import wraps
from flask import flash
from flask import Flask
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for
from http import HTTPStatus
import requests


APP = Flask(__name__)
APP.config.from_object('config')
BACKEND_URL = 'http://backend:5000'


def _make_request_with_auth(url, method, data={}):
    methods = {
        'post': requests.post,
        'get': requests.get,
        'put': requests.put,
        'delete': requests.delete
    }
    try:
        method = methods[method]
    except KeyError:
        raise AttributeError('Unkown request type')

    headers = {'session': session['session_id']}
    response = method(url, json=data, headers=headers)
    if response.status_code == HTTPStatus.FORBIDDEN:
        del session['session_id']
        del session['current_user']
        raise ValueError('Session has expired')
    else:
        return response


@APP.route('/')
def home():
    return render_template('index.html')


@APP.route('/login', methods = ['POST'])
def login():
    user_name = request.form.get('id')
    password = request.form.get('pw')
    
    if user_name and password:
        response = requests.post(
            f'{BACKEND_URL}/users/{user_name}/login',
            headers={'password': password}
        )
        if response:
            session['current_user'] = user_name
            session['session_id'] = response.json()['session_id']
        else:
            flash(response.json()['message'])
    else:
        flash('Please enter a value for user name and password')

    return render_template('index.html')


@APP.route('/register', methods = ['POST'])
def register():
    user_name = request.form.get('id')
    password = request.form.get('pw')
    
    if user_name and password:
        response = requests.post(
            f'{BACKEND_URL}/users',
            json={'user_name': user_name},
            headers={'password': password}
        )
        if response:
            flash('Account created, please log in')
        else:
            print(response.text, flush=True)
    else:
        flash('Please enter a value for user name and password')

    return render_template('index.html')


@APP.route('/logout')
def logout():
    try:
        response = _make_request_with_auth(
            f'{BACKEND_URL}/users/logout',
            method='post'
        )
        if response:
            del session['current_user']
            del session['session_id']
            flash('Logout Successful!')
        else:
            flash('An error occured')
            print(response.text, flush=True)
    except ValueError:
        # Nothing to do - user was logging out anyway
        pass
    return render_template('index.html')


@APP.route('/view-media')
def view():
    return render_template('view-media.html')