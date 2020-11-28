from flask import jsonify
from flask import request
from http import HTTPStatus
from .auth import validate_session
from .auth import end_session
from .user import User


def create_user():
    try:
        user_name = request.json['user_name']
        password = request.headers['password']
        User.create(user_name, password)
        response = {'user_name': user_name}
        code = HTTPStatus.CREATED
    except KeyError:
        response = {'message': "The user could not be created because the request was invalid"}
        code = HTTPStatus.BAD_REQUEST
    except ValueError:
        response = {'message': "The user could not be created because the user name exists"}
        code = HTTPStatus.CONFLICT
    return jsonify(response), code


def login_user(user_name: str):
    try:
        password = request.headers['password']
        session_id = User.log_in_user(user_name, password)
        response = {
            'session_id': session_id
        }
        code = HTTPStatus.OK
    except KeyError:
        response = {'message': "The user could not be logged in because no password was given"}
        code = HTTPStatus.BAD_REQUEST
    except ValueError as e:
        response = {'message': str(e)}
        code = HTTPStatus.UNAUTHORIZED
    return jsonify(response), code


def logout_user():
    session_id = request.headers['session'].split()
    end_session(session_id)
    return {}, HTTPStatus.NO_CONTENT
