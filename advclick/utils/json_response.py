from flask import jsonify

BAD_REQUEST = 400
PAGE_NOT_FOUND = 404
INTERNAL_SERVER_ERROR = 500
SERVICE_UNAVAILABLE = 503
SERVER_ERROR_MSG = 1001


def get_error_msg(message, code=INTERNAL_SERVER_ERROR, data={}):
    if message is None:
        message = 'Unknown Error !'
    result = jsonify(code=code, message=message, data=data)
    return result


def get_success_msg(message, code=0, data={}):
    if message is None:
        message = 'Operate success!'
    result = jsonify(code=code, message=message, data=data)
    return result


def get_success_data(data):
    if data is None:
        data = {}
    result = jsonify(code=0, message='Success', data=data)
    return result
