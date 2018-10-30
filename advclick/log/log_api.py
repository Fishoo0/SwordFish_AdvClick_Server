from flask import Blueprint, request

from advclick.log import log
from advclick.utils import json_response

bp = Blueprint('log', __name__, url_prefix='/log')


@bp.route("/get_logs", methods=('GET', 'POST'))
def get_logs():
    print('get_logs')
    content = request.get_json()
    if content is None:
        return json_response.get_error_msg('Invalid request')
    print(content)
    user_id = content.get('user_id', '')
    result = log.get_logs(user_id)
    return json_response.get_response(result)
