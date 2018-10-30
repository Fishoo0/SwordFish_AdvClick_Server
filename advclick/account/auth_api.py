import json

from flask import (
    Blueprint, request)

from advclick.account import auth
from advclick.log import log
from advclick.utils import json_response, string_utils

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
    if isinstance(result, dict):
        log.add_log(result['id'], 'register', content.get('ip'), content.get('location'))
        return json_response.get_success_data(data=result, message='Register successfully!')
    else:
        return json_response.get_error_msg(result)


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
    if isinstance(result, dict):
        log.add_log(result['id'], 'login', content.get('ip'), content.get('location'))
        return json_response.get_success_data(data=result, message='Login Success')
    else:
        return json_response.get_error_msg(result)


@bp.route("/logout", methods=('GET', 'POST'))
def logout():
    print('logout')
    content = request.get_json()
    if content is None:
        return json_response.get_error_msg('Invalid request')
    request_id = content.get('id')
    result = auth.logout(request_id)
    if isinstance(result, dict):
        log.add_log(request_id, 'logout', content.get('ip'), content.get('location'))
        return json_response.get_success_msg('Logout successfully!', data=result)
    else:
        return json_response.get_error_msg(result)


@bp.route("/get_user", methods=('GET', 'POST'))
def get_user():
    print("get_user")
    content = request.get_json()
    if content is None:
        return json_response.get_error_msg('Invalid request')
    print(content)
    request_id = content.get('id')
    result = auth.find_user(request_id=request_id)
    if isinstance(result, dict):
        return json_response.get_success_data(result)
    else:
        return json_response.get_error_msg(result)


@bp.route("/update_profile", methods=('GET', 'POST'))
def update_profile():
    print("update_profile")
    content = request.get_json()
    if content is None:
        return json_response.get_error_msg('Invalid request')
    print(content)
    request_id = content.get('id')
    request_password = content.get('password')
    request_im_qq = content.get('im_qq')
    request_telephone = content.get('telephone')

    request_alipay = content.get('alipay')
    request_alipay_name = content.get('alipay_name')
    request_prime_level = content.get('prime_level')
    request_prime_period = content.get('prime_period')
    request_youmeng_checked = content.get('youmeng_checked')

    result = auth.update_profile(request_id, request_password, request_im_qq, request_telephone, request_alipay,
                                 request_alipay_name, request_prime_level, request_prime_period,
                                 request_youmeng_checked)
    return json_response.get_response(result)


@bp.route("/check_youmeng", methods=('GET', 'POST'))
def check_youmeng():
    print("check_youmeng")
    content = request.get_json()
    if content is None:
        return json_response.get_error_msg('Invalid request')
    print(content)
    request_id = content.get('id')
    baidu = content.get('youmeng_baidu')
    google = content.get('youmeng_google')
    sougou = content.get('youmeng_sougou')
    taobao = content.get('youmeng_taobao')
    result = auth.check_youmeng(request_id, baidu, google, sougou, taobao)
    if isinstance(result, dict):
        return json_response.get_success_data(result)
    elif isinstance(result, str):
        return json_response.get_error_msg(result)
    else:
        return json_response.get_error_msg(result)
