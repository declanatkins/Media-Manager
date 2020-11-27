from functools import wraps
from flask import request
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
            raise ValueError('No authentication provided')
