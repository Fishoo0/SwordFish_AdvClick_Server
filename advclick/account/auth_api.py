import json

from flask import (
    Blueprint, request
)

from advclick.account import auth
from advclick.utils import json_response

bp = Blueprint('auth', __name__, url_prefix='/auth')

def check_params(user_name, user_password=None, check_password=True):
    if user_name is None:
        return json_response.get_error_msg('Invalid user_name')
    if (user_password is None or user_password is '') and check_password:
        return json_response.get_error_msg('Invalid user_password')
    return None


@bp.route("/register", methods=('GET', 'POST'))
def register():
    print("register")
    content = request.get_json()
    if content is None:
        return json_response.get_error_msg('Invalid request')
    user_name = content.get('user_name')
    user_password = content.get('user_password')
    check_result = check_params(user_name, user_password)
    if check_result is not None:
        return check_result

    result = auth.register(user_name, user_password)
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
    user_name = content.get('user_name')
    user_password = content.get('user_password')
    check_result = check_params(user_name, user_password, check_password=False)
    if check_result is not None:
        return check_result
    result = login(user_name, user_password)
    if result is not None:
        return json_response.get_error_msg(result)
    return json_response.get_success_msg('Login successfully!')


@bp.route("/logout", methods=('GET', 'POST'))
def logout():
    print('logout')
    content = request.get_json()
    if content is None:
        return json_response.get_error_msg('Invalid request')
    user_name = content.get('user_name')
    check_result = check_params(user_name, check_password=False)
    if check_result is not None:
        return check_result
    result = logout(user_name)
    if result is not None:
        return json_response.get_error_msg(result)
    return json_response.get_success_msg('Logout successfully!', data=json.dumps({'user_name': user_name}))
