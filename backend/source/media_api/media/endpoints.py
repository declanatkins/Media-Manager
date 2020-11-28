from http import HTTPStatus
from flask import jsonify
from flask import request
from .game import Game
from .movie import Movie
from .song import Song
from ..users.auth import validate_session


TYPES_DICT = {
    'Game': Game,
    'Movie': Movie,
    'Song': Song
}


def create_media():
    validation_response = validate_session()
    if not validation_response.success:
        return validation_response.response, validation_response.code
    else:
        session_user = validation_response.user
    try:
        json_ = request.json
        media_type = json_.pop('type')
        media_object = TYPES_DICT[media_type](**json_)
        session_user.create_media(media_object)
        response = media_object.as_json()
        code = HTTPStatus.CREATED
    except KeyError:
        response = {'message': 'Invalid media type'}
        code = HTTPStatus.BAD_REQUEST
    return jsonify(response), code


def search_media():
    validation_response = validate_session()
    if not validation_response.success:
        return validation_response.response, validation_response.code
    else:
        session_user = validation_response.user
    media = session_user.media
    filtered_media = []
    for media_item in media:
        for filter_param in request.args:
            if filter_param not in media_item:
                break
            if not request.args[filter_param] in media_item[filter_param]:
                break
        else:  # no break
            filtered_media.append(media_item)
    return jsonify(filtered_media), HTTPStatus.OK


def search_media_by_type(media_type):
    validation_response = validate_session()
    if not validation_response.success:
        return validation_response.response, validation_response.code
    else:
        session_user = validation_response.user
    media = session_user.media
    typed_media = [media_item for media_item in media if media_item['type'] == media_type]
    filtered_media = []
    for media_item in typed_media:
        for filter_param in request.args:
            if filter_param not in media_item:
                break
            if not request.args[filter_param] in media_item[filter_param]:
                break
        else:  # no break
            filtered_media.append(media_item)
    return jsonify(filtered_media), HTTPStatus.OK


def get_media_by_id(media_id):
    validation_response = validate_session()
    if not validation_response.success:
        return validation_response.response, validation_response.code
    else:
        session_user = validation_response.user
    try:
        response = session_user.read_media(media_id)
        code = HTTPStatus.OK
    except ValueError:
        response = {'message': 'Could not find the media item'}
        code = HTTPStatus.NOT_FOUND
    return jsonify(response), code


def update_media_by_id(media_id):
    validation_response = validate_session()
    if not validation_response.success:
        return validation_response.response, validation_response.code
    else:
        session_user = validation_response.user
    try:
        json_ = request.json
        media_type = json_.pop('type')
        media_object = TYPES_DICT[media_type](id_=media_id, **json_)
        session_user.update_media(media_object)
        response = media_object.as_json()
        code = HTTPStatus.OK
    except KeyError:
        response = {'message': 'Invalid media type'}
        code = HTTPStatus.BAD_REQUEST
    except ValueError:
        response = {'message': 'Could not find the media item'}
        code = HTTPStatus.NOT_FOUND
    return jsonify(response), code


def delete_media_by_id(media_id):
    validation_response = validate_session()
    if not validation_response.success:
        return validation_response.response, validation_response.code
    else:
        session_user = validation_response.user
    try:
        session_user.delete_media(media_id)
        response = {}
        code = HTTPStatus.NO_CONTENT
    except ValueError:
        response = {'message': 'Could not find the media item'}
        code = HTTPStatus.NOT_FOUND
    return jsonify(response), code
