from flask import Blueprint, request, jsonify
from pip._vendor.urllib3.util import url

from advclick.account import auth
from advclick.click import click, click_api
from advclick.utils import json_response

bp = Blueprint('manager', __name__, url_prefix='/manager')


@bp.route("/get_users", methods=('GET', 'POST'))
def get_users():
    print("get_users")
    content = request.get_json()
    if content is None:
        return json_response.get_error_msg('Invalid request')
    print(content)
    user_id = content.get('user_id')
    result = auth.find_users(user_id=user_id)
    if result is None:
        return json_response.get_error_msg('Can not find User')
    return json_response.get_success_msg(jsonify(result))


@bp.route("/upload_with_draw_times", methods=('GET', 'POST'))
def upload_with_draw_times():
    print("upload_with_draw_times")
    return click_api.upload_earn()
