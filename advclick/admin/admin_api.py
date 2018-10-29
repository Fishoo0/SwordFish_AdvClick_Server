from flask import Blueprint, request

from advclick.admin import admin
from advclick.click import click
from advclick.utils import json_response

bp = Blueprint('admin', __name__, url_prefix='/admin')


@bp.route("/get_users", methods=('GET', 'POST'))
def get_users():
    print("get_users")
    content = request.get_json()
    if content is None:
        return json_response.get_error_msg('Invalid request')
    print(content)
    request_user_id = content.get('user_id')
    result = admin.find_users(request_user_id)
    if isinstance(result, dict) or isinstance(result, list):
        return json_response.get_success_data(result)
    else:
        return json_response.get_error_msg(result)


@bp.route("/update_money", methods=('GET', 'POST'))
def update_money():
    print('update_money')
    content = request.get_json()
    if content is None:
        return json_response.get_error_msg('Invalid request')
    print(content)
    request_user_id = content.get('user_id')
    request_earn_amount = content.get('earn_amount', -1)
    request_with_draw_times_left = content.get('with_draw_times_left', -1)
    request_request_with_draw_amount = content.get('request_with_draw_amount', -1)
    return json_response.get_response(
        click.update_click(request_user_id, request_earn_amount, request_with_draw_times_left,
                           request_request_with_draw_amount))


@bp.route("/onekey_withdraw", methods=('GET', 'POST'))
def onekey_withdraw():
    print('onekey_withdraw')
    content = request.get_json()
    if content is None:
        return json_response.get_error_msg('Invalid request')
    print(content)
    request_user_id = content.get('user_id')
    return json_response.get_response(
        click.onekey_withdraw(request_user_id))
