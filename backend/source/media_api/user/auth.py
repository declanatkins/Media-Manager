from functools import wraps
from time import time
from flask import jsonify
from flask import request
from http import HTTPStatus
from pymongo import MongoClient
from .. import config
from .user import User


CLIENT = MongoClient(host=config.MONGODB_HOST, port=config.MONGODB_PORT)
DB = CLIENT[config.MONGODB_DB_NAME]


def validate_session(func):
    """
    Decorator for validating the supplied user session
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            _, session_id = request.headers['Authorization'].split()
        except KeyError:
            response = jsonify({
                'status': HTTPStatus.FORBIDDEN,
                'description': 'No authorization was provided'
            })
            return response, HTTPStatus.FORBIDDEN
        session_collection = DB[config.MONGODB_SESSION_COLLECTION_NAME]
        session_doc = session_collection.find_one({'_id': session_id})
        
        if not session_doc:
            response = jsonify({
                'status': HTTPStatus.FORBIDDEN,
                'description': 'User is not in an active session'
            })
            return response, HTTPStatus.FORBIDDEN
            
        if time() > session_doc['last_access'] + config.SESSION_INACTIVE_TIMEOUT:
            response = jsonify({
                'status': HTTPStatus.FORBIDDEN,
                'description': 'User\'s session has timed out'
            })
            session_collection.delete_one({'_id': session_id})
            return response, HTTPStatus.FORBIDDEN
        request.session_context = User.retrieve_validated_user(session_doc['user_name'])
        return func(*args, **kwargs)
    return wrapper


def end_session(session_id: str):
    """End the session and log out the user
    """
    session_collection = DB[config.MONGODB_SESSION_COLLECTION_NAME]
    session_collection.delete_one({'_id': session_id})
    