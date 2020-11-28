from collections import namedtuple
from time import time
from flask import jsonify
from flask import request
from http import HTTPStatus
from pymongo import MongoClient
from .. import config
from .user import User


CLIENT = MongoClient(host=config.MONGODB_HOST, port=config.MONGODB_PORT)
DB = CLIENT[config.MONGODB_DB_NAME]


ValidationResponse = namedtuple('ValidationResponse', ['user', 'success', 'response', 'code'])


def validate_session() -> ValidationResponse:
    """
    Validates the supplied user session
    """
    try:
        session_id = request.headers['session']
    except KeyError:
        response = jsonify({
            'message': 'No authorization was provided'
        })
        return ValidationResponse('', False, response, HTTPStatus.FORBIDDEN)
    session_collection = DB[config.MONGODB_SESSION_COLLECTION_NAME]
    session_doc = session_collection.find_one({'_id': session_id})

    if not session_doc:
        response = jsonify({
            'message': 'User is not in an active session'
        })
        return ValidationResponse('', False, response, HTTPStatus.FORBIDDEN)

    if time() > session_doc['last_access'] + config.SESSION_INACTIVE_TIMEOUT:
        response = jsonify({
            'message': 'User\'s session has timed out'
        })
        session_collection.delete_one({'_id': session_id})
        return ValidationResponse('', False, response, HTTPStatus.FORBIDDEN)
    try:
        session_user = User.retrieve_validated_user(session_doc['user_name'])
    except ValueError:
        session_collection.delete_one({'_id': session_id})
        response = jsonify({
            'message': 'User is not in an active session'
        })
        return ValidationResponse('', False, response, HTTPStatus.FORBIDDEN)
    session_collection.update_one({'_id': session_id}, {'$set': {'last_access': time()}})
    return ValidationResponse(session_user, True, None, None)


def end_session(session_id: str):
    """End the session and log out the user
    """
    session_collection = DB[config.MONGODB_SESSION_COLLECTION_NAME]
    session_collection.delete_one({'_id': session_id})
