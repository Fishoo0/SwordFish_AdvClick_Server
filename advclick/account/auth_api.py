import json

from flask import (
    Blueprint, request,
    jsonify)

from advclick.account import auth
from advclick.utils import json_response, json_utils, string_utils

bp = Blueprint('auth', __name__, url_prefix='/auth')


def check_params(request_name, request_password=None, check_password=True):
    if request_name is None:
        return json_response.get_error_msg('Invalid user_name')
    if (request_password is None or request_password is '') and check_password:
        return json_response.get_error_msg('Invalid user_password')
    return None


@bp.route("/register", methods=('GET', 'POST'))
def register():
    print("register")
    content = request.get_json()
    if content is None:
        return json_response.get_error_msg('Invalid request')
    name = content.get('name')
    password = content.get('password')
    im_qq = content.get('im_qq')
    alipay = content.get('alipay')
    alipay_name = content.get('alipay_name')

    check_result = check_params(name, password)
    if check_result is not None:
        return check_result

    if string_utils.is_empty(im_qq):
        return json_response.get_error_msg('Invalid im_qq')
    if string_utils.is_empty(alipay):
        return json_response.get_error_msg('Invalid alipay')
    if string_utils.is_empty(alipay_name):
        return json_response.get_error_msg('Invalid alipay_name')

    result = auth.find_user(request_name=name)
    if result is not None:
        return json_response.get_error_msg(
            'This name [' + name + ']  has been registered yet, please login or change another name.')

    result = auth.register(name, password, im_qq, alipay, alipay_name)
    if result is not None:
        return json_response.get_error_msg(result)
    return json_response.get_success_msg('Register successfully!')


@bp.route("/login", methods=('GET', 'POST'))
def login():
    print("login")
    content = request.get_json()
    if content is None:
        return json_response.get_error_msg('Invalid request')
    print(content)
    name = content.get('name')
    password = content.get('password')
    check_result = check_params(name, password, check_password=False)
    if check_result is not None:
        return check_result
    result = auth.login(name, password)
    if result is not None:
        return json_response.get_error_msg(result)
    return json_response.get_success_data(auth.find_user(request_name=name, to_dict=True))


@bp.route("/logout", methods=('GET', 'POST'))
def logout():
    print('logout')
    content = request.get_json()
    if content is None:
        return json_response.get_error_msg('Invalid request')
    name = content.get('name')
    check_result = check_params(name, check_password=False)
    if check_result is not None:
        return check_result
    result = auth.logout(name)
    if result is not None:
        return json_response.get_error_msg(result)
    return json_response.get_success_msg('Logout successfully!', data=json.dumps({'user_name': name}))


@bp.route("/get_user", methods=('GET', 'POST'))
def get_user():
    print("get_user")
    content = request.get_json()
    if content is None:
        return json_response.get_error_msg('Invalid request')
    print(content)
    request_id = content.get('id')
    result = auth.find_user(request_id=request_id)
    if result is None:
        return json_response.get_error_msg('Can not find User')
    return json_response.get_success_msg(jsonify(result))
