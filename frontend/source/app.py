from functools import wraps
from flask import flash
from flask import Flask
from flask import render_template
from flask import request
from flask import session
from flask import url_for
from http import HTTPStatus
import requests


APP = Flask(__name__, static_url_path='/static')
APP.config.from_object('config')
BACKEND_URL = 'http://backend:5000'


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'session_id' not in session:
            flash('Login Required')
            return render_template('index.html')
        return func(*args, **kwargs)
    return wrapper


def _make_request_with_auth(url, method, data={}, params={}):
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
    response = method(url, json=data, headers=headers, params=params)
    if response.status_code == HTTPStatus.FORBIDDEN:
        del session['session_id']
        del session['current_user']
        raise ValueError('Session has expired')
    else:
        return response


def _create_media_object(type_):
    media_object = {key: value for key, value in request.form.items()}
    media_object['type'] = type_
    if not media_object['name']:
        flash('A name must be provided')
        return render_template(f'create-{type_.lower()}.html')

    thumbail_file = request.files.get('thumbnail')
    if thumbail_file:
        response = requests.post(
            f'{BACKEND_URL}/files/{thumbail_file.filename}',
            data=thumbail_file.read()
        )
        if not response:
            flash("Couldn't create thumbail, please try again")
            return render_template(f'create-{type_.lower()}.html')
        media_object['thumbnail_path'] = response.json()['file_id']
    else:
         media_object['thumbnail_path'] = ''
    try:
        response = _make_request_with_auth(f'{BACKEND_URL}/media', 'post', data=media_object)
    except ValueError:
        flash('Session Expired')
        return render_template('index.html')
    if not response:
        flash("Couldn't create media, please try again")
        return render_template(f'create-{type_.lower()}.html')
    return render_template('create-media.html')


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
            flash('An error occurred, please try again')
    else:
        flash('Please enter a value for user name and password')

    return render_template('index.html')


@APP.route('/logout')
@login_required
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
    except ValueError:
        # Nothing to do - user was logging out anyway
        pass
    return render_template('index.html')


@APP.route('/view-media')
@login_required
def view():
    try:
        if request.args and request.args.get('type') != 'All':
            url = f'{BACKEND_URL}/media/types/{request.args.get("type")}'
        else:
            url = f'{BACKEND_URL}/media'
        params = {}
        if request.args and request.args.get('name'):
            params['name'] = request.args.get('name')
        response = _make_request_with_auth(url, 'get', params=params)
    except ValueError:
        flash('Session Expired')
        return render_template('index.html')
    if response:
        results = response.json()
        for result in results:
            if result['thumbnail_path']:
                result['thumbnail_path'] = f'http://localhost:5000/files/{result["thumbnail_path"]}'
            else:
                result['thumbnail_path'] = url_for('static', filename=f'img/{result["type"].lower()}.png')
        return render_template('view-media.html', results=results)
    else:
        flash('An error occurred')
        return render_template('index.html')


@APP.route('/create-media')
@login_required
def create():
    return render_template('create-media.html')


@APP.route('/create-game')
@login_required
def create_game():
    return render_template('create-game.html')


@APP.route('/create-music')
@login_required
def create_music():
    return render_template('create-song.html')


@APP.route('/create-movie')
@login_required
def create_movie():
    return render_template('create-movie.html')


@APP.route('/create-game-object', methods=['POST'])
@login_required
def create_game_object():
    return _create_media_object('Game')


@APP.route('/create-music-object', methods=['POST'])
@login_required
def create_music_object():
    return _create_media_object('Song')


@APP.route('/create-movie-object', methods=['POST'])
@login_required
def create_movie_object():
    return _create_media_object('Movie')


@APP.route('/edit-media-page')
@login_required
def edit_media_page():
    if not request.args or not request.args.get('id'):
        flash('Invalid media parameters')
        return render_template('index.html')
    try:
        response = _make_request_with_auth(
            f'{BACKEND_URL}/media/{request.args.get("id")}',
            'get'
        )
        if not response:
            flash('Failed to retrieve media')
            return render_template('index.html')
    except ValueError:
        flash('Session Expired')
        return render_template('index.html')
    
    print(response.json(), flush=True)
    return render_template('edit-media.html', media=response.json())


@APP.route('/edit-media', methods=['POST'])
@login_required
def edit_media():
    media_object = {key: value for key, value in request.form.items()}
    media_id = media_object.pop('id')

    if request.files.get('thumbnail'):
        if request.form.get('thumbnail_path'):
            response = requests.delete(f'{BACKEND_URL}/files/{request.form.get("thumbnail_path")}')
            if not response:
                flash('Failed to delete old thumbnail')
                return render_template('index.html')
            response = requests.post(
                f'{BACKEND_URL}/files/{request.files.get("thumbnail").filename}',
                data=request.files.get('thumbnail').read()
            )
            if not response:
                flash("Couldn't create thumbail, please try again")
                return render_template(f'index.html')
            media_object['thumbnail_path'] = response.json()['file_id']
    
    response = _make_request_with_auth(
        f'{BACKEND_URL}/media/{media_id}',
        method='put',
        data=media_object
    )
    if response:
        flash('Media successfully edited')
    else:
        flash('An error occurred')
    return render_template('index.html')


@APP.route('/delete-media', methods=['POST'])
@login_required
def delete_media():
    media_id = request.form.get('id')
    thumbnail = request.form.get('thumbnail_path')

    if thumbnail:
        response = requests.delete(f'{BACKEND_URL}/files/{thumbnail}')
        if not response:
            flash('Failed to delete old thumbnail')
            return render_template('index.html')
    
    response = _make_request_with_auth(f'{BACKEND_URL}/media/{media_id}', method='delete')
    if response:
        flash('Media successfully deleted')
    else:
        flash('Failed to delete Media')
    return render_template('index.html')
