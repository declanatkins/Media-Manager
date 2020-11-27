from flask import jsonify
from flask import request
from .game import Game
from .movie import Movie
from .song import Song
from ..user.auth import validate_session


@validate_session
def create_media():
    pass


@validate_session
def get_all_media():
    pass


@validate_session
def get_all_media_by_type(media_type):
    pass


@validate_session
def search_media():
    pass


@validate_session
def search_media_by_type(media_type):
    pass
