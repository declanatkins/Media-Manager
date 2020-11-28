from mock import MagicMock, patch
import pytest
from media_api.users.auth import ValidationResponse
from media_api import main
from media_api.media.game import Game
from media_api.users.user import User


@pytest.fixture
def test_app():
    return main.APP.app.test_client()


def test_create_file(test_app):
    with open('Dockerfile', 'rb') as f:
        data = f.read()
    with patch('media_api.files.endpoints.open'), patch('media_api.files.endpoints.uuid4', return_value='1234'):
        response = test_app.post('/files/test_media.py', data=data)
        assert response.status_code == 201
        assert response.json == {
            'file_id': '1234.py'
        }


def test_delete_file(test_app):
    with patch('media_api.files.endpoints.os.remove'):
        response = test_app.delete('/files/test_media.py')
        assert response.status_code == 204


def test_delete_file_error(test_app):
    response = test_app.delete('/files/test_media.py')
    assert response.status_code == 404


def test_get_file(test_app):
    with patch('media_api.files.endpoints.send_from_directory', return_value='{}'):
        response = test_app.get('/files/test_media.py')
        assert response.status_code == 200


def test_get_file_error(test_app):
    response = test_app.delete('/files/test_media.py')
    assert response.status_code == 404


def test_create_user(test_app):
    user_name = 'user'
    password = 'password'
    with patch('media_api.users.endpoints.User.create'):
        response = test_app.post('/users', json={'user_name': user_name}, headers={'password': password})
        assert response.status_code == 201
        assert response.json == {'user_name': user_name}


def test_create_user_no_header(test_app):
    user_name = 'user'
    response = test_app.post('/users', json={'user_name': user_name})
    assert response.status_code == 400


def test_create_user_already_exists(test_app):
    user_name = 'user'
    password = 'password'
    with patch('media_api.users.endpoints.User.create') as create:
        create.side_effect = ValueError()
        response = test_app.post('/users', json={'user_name': user_name}, headers={'password': password})
    assert response.status_code == 409


def test_login_user(test_app):
    user_name = 'user'
    password = 'password'
    with patch('media_api.users.endpoints.User.log_in_user', return_value='session-id'):
        response = test_app.post(f'/users/{user_name}/login', json={'user_name': user_name}, headers={'password': password})
        assert response.status_code == 200
        assert response.json == {'session_id': 'session-id'}


def test_login_user_no_header(test_app):
    user_name = 'user'
    response = test_app.post(f'/users/{user_name}/login')
    assert response.status_code == 400


def test_login_user_fail(test_app):
    user_name = 'user'
    password = 'password'
    with patch('media_api.users.endpoints.User.log_in_user') as login:
        login.side_effect = ValueError()
        response = test_app.post(f'/users/{user_name}/login', headers={'password': password})
    assert response.status_code == 401


def test_logout_user(test_app):
    with patch('media_api.users.endpoints.end_session'):
        response = test_app.post('/users/logout', headers={'session': '1234'})
        assert response.status_code == 204


def test_logout_user_no_header(test_app):
    with patch('media_api.users.endpoints.end_session'):
        response = test_app.post('/users/logout')
        assert response.status_code == 400


def test_create_media(test_app):
    test_media = Game('test_name', 'test_path', 'test_genres', 'test_platform', 'test_mult', 'test-id')
    media_json = test_media.as_json()
    del media_json['_id']
    with patch('media_api.media.endpoints.validate_session', return_value=ValidationResponse(MagicMock(), True, None, None)):
        response = test_app.post('/media', json=media_json, headers={'session': '1234'})
        assert response.status_code == 201
        got_json = response.json
        del got_json['_id']
        assert got_json == media_json


def test_create_media_bad_type(test_app):
    test_media = Game('test_name', 'test_path', 'test_genres', 'test_platform', 'test_mult', 'test-id')
    media_json = test_media.as_json()
    media_json['type'] = 'Frog'
    del media_json['_id']
    with patch('media_api.media.endpoints.validate_session', return_value=ValidationResponse(MagicMock(), True, None, None)):
        response = test_app.post('/media', json=media_json, headers={'session': '1234'})
        assert response.status_code == 400


def test_search_no_param(test_app):
    media_json = Game('test_name', 'test_path', 'test_genres', 'test_platform', 'test_mult', 'test-id').as_json()
    user = User(document={'media': [media_json]})
    with patch('media_api.media.endpoints.validate_session', return_value=ValidationResponse(user, True, None, None)):
        response = test_app.get('/media', headers={'session': '1234'})
        assert response.status_code == 200
        assert response.json == [media_json]


def test_search_with_param(test_app):
    media_json1 = Game('test_name', 'test_path', 'test_genres', 'test_platform', 'test_mult', 'test-id').as_json()
    media_json2 = Game('test_name1', 'test_path', 'test_genres', 'test_platform', 'test_mult', 'test-id').as_json()
    user = User(document={'media': [media_json1, media_json2]})
    with patch('media_api.media.endpoints.validate_session', return_value=ValidationResponse(user, True, None, None)):
        response = test_app.get('/media?name=test_name1', headers={'session': '1234'})
        assert response.status_code == 200
        assert response.json == [media_json2]


def test_search_by_type_no_param(test_app):
    media_json = Game('test_name', 'test_path', 'test_genres', 'test_platform', 'test_mult', 'test-id').as_json()
    user = User(document={'media': [media_json]})
    with patch('media_api.media.endpoints.validate_session', return_value=ValidationResponse(user, True, None, None)):
        response = test_app.get('/media/types/Game', headers={'session': '1234'})
        assert response.status_code == 200
        assert response.json == [media_json]


def test_search_by_type_with_param(test_app):
    media_json1 = Game('test_name', 'test_path', 'test_genres', 'test_platform', 'test_mult', 'test-id').as_json()
    media_json2 = Game('test_name1', 'test_path', 'test_genres', 'test_platform', 'test_mult', 'test-id').as_json()
    user = User(document={'media': [media_json1, media_json2]})
    with patch('media_api.media.endpoints.validate_session', return_value=ValidationResponse(user, True, None, None)):
        response = test_app.get('/media/types/Game?name=test_name1', headers={'session': '1234'})
        assert response.status_code == 200
        assert response.json == [media_json2]


def test_get_media_by_id(test_app):
    media_json1 = Game('test_name', 'test_path', 'test_genres', 'test_platform', 'test_mult', 'test-id').as_json()
    user = User(document={'media': [media_json1]})
    with patch('media_api.media.endpoints.validate_session', return_value=ValidationResponse(user, True, None, None)):
        response = test_app.get(f'/media/{media_json1["_id"]}', headers={'session': '1234'})
        assert response.status_code == 200
        assert response.json == media_json1


def test_get_media_by_id_not_found(test_app):
    user = User(document={'media': []})
    with patch('media_api.media.endpoints.validate_session', return_value=ValidationResponse(user, True, None, None)):
        response = test_app.get(f'/media/1234', headers={'session': '1234'})
        assert response.status_code == 404


def test_update_media(test_app):
    test_media = Game('test_name', 'test_path', 'test_genres', 'test_platform', 'test_mult', 'test-id')
    media_json = test_media.as_json()
    del media_json['_id']
    with patch('media_api.media.endpoints.validate_session', return_value=ValidationResponse(MagicMock(), True, None, None)):
        response = test_app.put(f'/media/{test_media.id_code}', json=media_json, headers={'session': '1234'})
        assert response.status_code == 200
        got_json = response.json
        del got_json['_id']
        assert got_json == media_json


def test_update_media_bad_type(test_app):
    test_media = Game('test_name', 'test_path', 'test_genres', 'test_platform', 'test_mult', 'test-id')
    media_json = test_media.as_json()
    media_json['type'] = 'Frog'
    del media_json['_id']
    with patch('media_api.media.endpoints.validate_session', return_value=ValidationResponse(MagicMock(), True, None, None)):
        response = test_app.put(f'/media/{test_media.id_code}', json=media_json, headers={'session': '1234'})
        assert response.status_code == 400


def test_delete_media(test_app):
    test_media = Game('test_name', 'test_path', 'test_genres', 'test_platform', 'test_mult', 'test-id')
    media_json = test_media.as_json()
    del media_json['_id']
    with patch('media_api.media.endpoints.validate_session', return_value=ValidationResponse(MagicMock(), True, None, None)):
        response = test_app.delete(f'/media/{test_media.id_code}', headers={'session': '1234'})
        assert response.status_code == 204