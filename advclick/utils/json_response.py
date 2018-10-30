import array
from flask import jsonify

BAD_REQUEST = 400
PAGE_NOT_FOUND = 404
INTERNAL_SERVER_ERROR = 500
SERVICE_UNAVAILABLE = 503
SERVER_ERROR_MSG = 1001


def get_error_msg(message, code=INTERNAL_SERVER_ERROR, data=None):
    if message is None:
        message = 'Unknown Error !'
    result = jsonify(code=code, message=message, data=data)
    return result


def get_success_msg(message, code=0, data=None):
    if message is None:
        message = 'Operate success!'
    result = jsonify(code=code, message=message, data=data)
    return result


def get_success_data(data=None, message='Success'):
    result = jsonify(code=0, message=message, data=data)
    return result


def get_response(result):
    if isinstance(result, dict) or isinstance(result, list):
        return get_success_data(result)
    else:
        return get_error_msg(message=result)
