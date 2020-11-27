import os
import hashlib
from time import time
from uuid import uuid4
from pymongo import MongoClient

from .. import config
from ..media.abc import MediaItem


CLIENT = MongoClient(host=config.MONGODB_HOST, port=config.MONGODB_PORT)
DB = CLIENT[config.MONGODB_DB_NAME]


def _get_user_document(user_name):
    user_collection = DB[config.MONGODB_USER_COLLECTION_NAME]
    user_document = user_collection.find_one({'_id': user_name})
    return user_document


class User:
    """Class for a user of the media app
    """

    @staticmethod
    def create(user_name: str, password: str) -> str:
        """Create a new user for the application

        Args:
            user_name (str): name for the user
            password (str): password for the user

        Returns:
            (str): session id for the new session
        """
        if _get_user_document(user_name):
            raise ValueError('The user already exists')
        
        salt = os.urandom(32)
        key = hashlib.pbkdf2_hmac(
            has_name='sha256',
            password=password.encode('utf-8'),
            salt=salt,
            iterations=100000,
            dklen=128
        )
        user_object = {
            '_id': user_name,
            'salt': salt,
            'key': key,
            'media': []
        }
        user_collection = DB[config.MONGODB_USER_COLLECTION_NAME]
        user_collection.insert_one(user_object)
    
    @staticmethod
    def retrieve_validated_user(user_name: str):
        pass
    
    
    @staticmethod
    def log_in_user(user_name: str, password: str):
        pass

    def __init__(self, user_name: str):
        self._user_name = user_name
    
    def update_password(self, new_password: str):
        pass

    def create_media(self, media: MediaItem):
        pass

    def read_media(self, media_id: str):
        pass
    
    def update_media(self, media: MediaItem):
        pass

    def delete_media(self, media_id: str):
        pass
