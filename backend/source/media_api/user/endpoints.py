from flask import jsonify
from flask import request
from http import HTTPStatus
from .auth import validate_session
from .auth import end_session
from .user import User


def create_user():
    try:
        user_name = request.json['user_name']
        _, password = request.headers['Authorization'].split()
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
        _, password = request.headers['Authorization'].split()
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


@validate_session
def logout_user(user_name):
    _, session_id = request.headers['Authorization'].split()
    end_session(session_id)
    return {}, HTTPStatus.NO_CONTENT


@validate_session
def rename_user():
    user_name = request.json['user_name']
    try:
        request.session_user.update_user_name(user_name)
        response = {'user_name': user_name}
        code = HTTPStatus.OK
    except ValueError as e:
        response = {'message': f'Invalid user name: {str(e)}'}
        code = HTTPStatus.BAD_REQUEST
    return jsonify(response), code
