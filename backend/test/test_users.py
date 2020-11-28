import os
import hashlib
from _pytest.mark import param
import pytest
from mock import patch
from mock import MagicMock
from media_api.users import user
from media_api import config
from media_api.media.game import Game


def test_create_invalid_username():
    with pytest.raises(ValueError):
        user.User.create('', 'value')


def test_create_invalid_password():
    with pytest.raises(ValueError):
        user.User.create('value', '')


def test_create_user_exists():
    with pytest.raises(ValueError), patch.object(user, '_get_user_document', return_value='a value'):
        user.User.create('value', 'value')


def test_create():
    with patch.object(user, '_get_user_document', return_value=None), \
            patch.object(os, 'urandom', return_value=b'\x14'), \
            patch.object(user, 'DB', {config.MONGODB_USER_COLLECTION_NAME: MagicMock()}):
        user.User.create('value', 'value')
        assert user.DB[config.MONGODB_USER_COLLECTION_NAME].called_once_with({
            '_id': 'value',
            'salt': b'\x14',
            'key': b'\x14',
            'media': []
        })


def test_get_validated_user():
    with patch.object(user, '_get_user_document', return_value={'test': 'test'}):
        user_ = user.User.retrieve_validated_user('test')
        assert user_._document == {'test': 'test'}

    
def test_get_validated_user_error():
    with patch.object(user, '_get_user_document', return_value={}), \
            pytest.raises(ValueError):
        user_ = user.User.retrieve_validated_user('test')


def test_login_user_no_user_exists():
    with patch.object(user, '_get_user_document', return_value={}), \
            pytest.raises(ValueError):
        user.User.log_in_user('v', 'p')


def test_login_user_bad_password():
    with patch.object(user, '_get_user_document', return_value={'key': 'p', 'salt': 's'}), \
            patch.object(hashlib, 'pbkdf2_hmac', return_value='not p'), \
            pytest.raises(ValueError):
        user.User.log_in_user('v', 'p')


def test_login_user():
    with patch.object(user, '_get_user_document', return_value={'key': 'p', 'salt': 's'}), \
            patch.object(hashlib, 'pbkdf2_hmac', return_value='p'), \
            patch.object(user, 'DB', {config.MONGODB_SESSION_COLLECTION_NAME: MagicMock()}):
        user.User.log_in_user('v', 'p')


def test_media_prop():
    test_user = user.User({'media': ['media-item']})
    assert test_user.media == ['media-item']


def test_create_media():
    test_media = Game('test_name', 'test_path', 'test_genres', 'test_platform', 'test_mult', 'test-id')
    test_user = user.User({'media': [], '_id': ''})
    with patch.object(user, 'DB', {config.MONGODB_USER_COLLECTION_NAME: MagicMock()}):
        test_user.create_media(test_media)
    assert test_user.media == [test_media.as_json()]


def test_read_media():
    test_media1 = Game('test_name', 'test_path', 'test_genres', 'test_platform', 'test_mult', 'test-id')
    test_media2 = Game('test_name', 'test_path', 'test_genres', 'test_platform', 'test_mult', 'test-id2')
    test_user = user.User({'media': [test_media1.as_json(), test_media2.as_json()], '_id': ''})
    result = test_user.read_media(test_media2.id_code)
    assert result == test_media2.as_json()

def test_read_media_error():
    test_media = Game('test_name', 'test_path', 'test_genres', 'test_platform', 'test_mult', 'test-id')
    test_user = user.User({'media': [test_media.as_json()], '_id': ''})
    with pytest.raises(ValueError):
        result = test_user.read_media('not an id code')

def test_update_media():
    test_media1 = Game('test_name', 'test_path', 'test_genres', 'test_platform', 'test_mult', 'test-id')
    test_media2 = Game('test_name', 'test_path', 'test_genres', 'test_platform', 'test_mult', 'test-id2')
    test_media2_updated = test_media2
    test_media2_updated._multiplayer = 'none'
    test_user = user.User({'media': [test_media1.as_json(), test_media2.as_json()], '_id': ''})
    with patch.object(user, 'DB', {config.MONGODB_USER_COLLECTION_NAME: MagicMock()}):
        test_user.update_media(test_media2_updated)
    assert test_user.media == [test_media1.as_json(), test_media2_updated.as_json()]

def test_update_media_error():
    test_media = Game('test_name', 'test_path', 'test_genres', 'test_platform', 'test_mult', 'test-id')
    test_media2 = Game('test_name', 'test_path', 'test_genres', 'test_platform', 'test_mult', 'test-id2')
    test_user = user.User({'media': [test_media.as_json()], '_id': ''})
    with pytest.raises(ValueError):
        test_user.update_media(test_media2)


def test_delete_media():
    test_media1 = Game('test_name', 'test_path', 'test_genres', 'test_platform', 'test_mult', 'test-id')
    test_media2 = Game('test_name', 'test_path', 'test_genres', 'test_platform', 'test_mult', 'test-id2')
    test_user = user.User({'media': [test_media1.as_json(), test_media2.as_json()], '_id': ''})
    with patch.object(user, 'DB', {config.MONGODB_USER_COLLECTION_NAME: MagicMock()}):
        test_user.delete_media(test_media2.id_code)
    assert test_user.media == [test_media1.as_json()]

def test_delete_media_error():
    test_media = Game('test_name', 'test_path', 'test_genres', 'test_platform', 'test_mult', 'test-id')
    test_user = user.User({'media': [test_media.as_json()], '_id': ''})
    with pytest.raises(ValueError):
        test_user.delete_media('not an id')
