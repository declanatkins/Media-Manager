import pytest
from media_api.media.game import Game
from media_api.media.movie import Movie
from media_api.media.song import Song


def test_game_generated_id():
    game = Game('test_name', 'test_path', 'test_genres', 'test_platform', 'test_mult')
    json_ = game.as_json()
    del json_['_id']  # this is randomly created
    expected_json = {
        'type': 'Game',
        'name': 'test_name',
        'thumbnail_path': 'test_path',
        'genres': 'test_genres',
        'platform': 'test_platform',
        'multiplayer': 'test_mult'
    }
    assert json_ == expected_json

def test_movie_generated_id():
    game = Movie('test_name', 'test_path', 'test_genres', 'test_platform', 'test_mult')
    json_ = game.as_json()
    del json_['_id']  # this is randomly created
    expected_json = {
        'type': 'Movie',
        'name': 'test_name',
        'thumbnail_path': 'test_path',
        'genres': 'test_genres',
        'director': 'test_platform',
        'starring': 'test_mult'
    }
    assert json_ == expected_json

def test_song_generated_id():
    game = Song('test_name', 'test_path', 'test_genres', 'test_platform', 'test_mult')
    json_ = game.as_json()
    del json_['_id']  # this is randomly created
    expected_json = {
        'type': 'Song',
        'name': 'test_name',
        'thumbnail_path': 'test_path',
        'genres': 'test_genres',
        'artist': 'test_platform',
        'album': 'test_mult'
    }
    assert json_ == expected_json


def test_game_exact_id():
    game = Game('test_name', 'test_path', 'test_genres', 'test_platform', 'test_mult', 'test-id')
    json_ = game.as_json()
    expected_json = {
        '_id': 'test-id',
        'type': 'Game',
        'name': 'test_name',
        'thumbnail_path': 'test_path',
        'genres': 'test_genres',
        'platform': 'test_platform',
        'multiplayer': 'test_mult'
    }
    assert json_ == expected_json

def test_movie_exact_id():
    game = Movie('test_name', 'test_path', 'test_genres', 'test_platform', 'test_mult', 'test-id')
    json_ = game.as_json()
    expected_json = {
        '_id': 'test-id',
        'type': 'Movie',
        'name': 'test_name',
        'thumbnail_path': 'test_path',
        'genres': 'test_genres',
        'director': 'test_platform',
        'starring': 'test_mult'
    }
    assert json_ == expected_json

def test_song_exact_id():
    game = Song('test_name', 'test_path', 'test_genres', 'test_platform', 'test_mult', 'test-id')
    json_ = game.as_json()
    expected_json = {
        '_id': 'test-id',
        'type': 'Song',
        'name': 'test_name',
        'thumbnail_path': 'test_path',
        'genres': 'test_genres',
        'artist': 'test_platform',
        'album': 'test_mult'
    }
    assert json_ == expected_json