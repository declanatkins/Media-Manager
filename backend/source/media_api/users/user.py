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
        if not user_name or not password:
            raise ValueError('Invalid username/password')
        if _get_user_document(user_name):
            raise ValueError('The user already exists')

        salt = os.urandom(32)
        key = hashlib.pbkdf2_hmac(
            hash_name='sha256',
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
        document = _get_user_document(user_name)
        if document:
            return User(document)
        raise ValueError('User Not found')

    @staticmethod
    def log_in_user(user_name: str, password: str):
        document = _get_user_document(user_name)
        if not document:
            raise ValueError('User not found')

        generated_key = hashlib.pbkdf2_hmac(
            hash_name='sha256',
            password=password.encode('utf-8'),
            salt=document['salt'],
            iterations=100000,
            dklen=128
        )

        if not generated_key == document['key']:
            raise ValueError('Incorrect Password')

        session_id = str(uuid4())
        session_obj = {
            '_id': session_id,
            'user_name': user_name,
            'last_access': time()
        }
        session_collection = DB[config.MONGODB_SESSION_COLLECTION_NAME]
        session_collection.insert_one(session_obj)
        return session_id

    def __init__(self, document: dict):
        self._document = document

    @property
    def media(self) -> list[dict]:
        return self._document['media']

    def create_media(self, media: MediaItem):
        self._document['media'].append(media.as_json())
        user_collection = DB[config.MONGODB_USER_COLLECTION_NAME]
        user_collection.update_one(
            {
                '_id': self._document['_id']
            },
            {
                '$set': {
                    'media': self._document['media']
                }
            }
        )

    def read_media(self, media_id: str) -> MediaItem:
        for media_item in self._document['media']:
            if media_item['_id'] == media_id:
                return media_item

        raise ValueError('The given media ID was not found')

    def update_media(self, media: MediaItem):
        for i, media_item in enumerate(self._document['media']):
            if media_item['_id'] == media.id_code:
                self._document['media'][i] = media.as_json()
                user_collection = DB[config.MONGODB_USER_COLLECTION_NAME]
                user_collection.update_one(
                    {
                        '_id': self._document['_id']
                    },
                    {
                        '$set': {
                            'media': self._document['media']
                        }
                    }
                )
                break
        else:  # no break
            raise ValueError('The given media object did not exist')

    def delete_media(self, media_id: str):
        for i, media_item in enumerate(self._document['media']):
            if media_item['_id'] == media_id:
                del self._document['media'][i]
                user_collection = DB[config.MONGODB_USER_COLLECTION_NAME]
                user_collection.update_one(
                    {
                        '_id': self._document['_id']
                    },
                    {
                        '$set': {
                            'media': self._document['media']
                        }
                    }
                )
                break
        else:  # no break
            raise ValueError('The given media id was not dound')
