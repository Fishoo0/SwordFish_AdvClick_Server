from flask import Blueprint, request, jsonify

from advclick.click import click
from advclick.utils import json_response

bp = Blueprint('click', __name__, url_prefix='/click')


@bp.route("/upload_earn", methods=('GET', 'POST'))
def upload_earn():
    content = request.get_json()
    if content is None:
        return json_response.get_error_msg('Invalid request')
    print(content)
    user_id = content.get('user_id')
    value = content.get('value')
    if user_id is None or value is None:
        return json_response.get_error_msg('Invalid params user_id -> ' + user_id + ' value -> ' + value)
    result = click.upload_earn(user_id, value)
    if result is not None:
        return json_response.get_success_msg('Success')
    return "Unknown Error"


@bp.route("/get_earn", methods=('GET', 'POST'))
def get_earn():
    content = request.get_json()
    if content is None:
        return json_response.get_error_msg('Invalid request')
    print(content)
    user_id = content.get('user_id')
    if user_id is None:
        return json_response.get_error_msg('Invalid params user_id -> ' + user_id)
    result = click.get_earn(user_id)
    if result is not None:
        return json_response.get_success_msg(jsonify(result))
    return json_response.get_error_msg('Error when get earn info')
