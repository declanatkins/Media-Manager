import os
from flask import jsonify
from flask import request
from flask import send_from_directory
from http import HTTPStatus
from uuid import uuid4
from .. import config


def create_file(file_name: str):
    extension = '.' + file_name.rsplit('.', 1)[1] if '.' in file_name else ''
    file_uuid = str(uuid4())
    new_name = f'{file_uuid}{extension}'
    with open(os.path.join(config.FILES_DIRECTORY, new_name), 'w') as data_f:
        data_f.write(request.data)
    return jsonify({'file_id': new_name}), HTTPStatus.CREATED


def delete_file(file_id: str):
    file_path = os.path.join(config.FILES_DIRECTORY, file_id)
    try:
        os.remove(file_path)
        response = {}
        code = HTTPStatus.NO_CONTENT
    except FileNotFoundError:
        response = {
            'message': 'The file could not be deleted because it was not found'
        }
        code = HTTPStatus.NOT_FOUND
    return jsonify(response), code


def get_file(file_id: str):
    try:
        response = send_from_directory(config.FILES_DIRECTORY, file_id)
    except FileNotFoundError:
        response = jsonify({
            'message': 'The file could not be retrived because it was not found'
        }), HTTPStatus.NOT_FOUND
    return response
