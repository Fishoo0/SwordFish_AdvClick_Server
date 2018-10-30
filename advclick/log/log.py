import sqlite3
import time

from advclick.account import auth
from advclick.db.db import get_db
from advclick.utils import json_utils


# Not safe, should be https or some encryption
def add_log(request_user_id, operation, ip, location):
    print('add_log user_id -> ' + str(
        request_user_id) + ' operation -> ' + operation + ' ip -> ' + ip + ' location -> ' + location)
    try:
        db = get_db()
        db.execute('insert into Log(user_id,operation,time,ip,location) values (?,?,?,?,?)',
                   (
                       request_user_id, operation, time.asctime(), ip, location))
        db.commit()
        return None
    except sqlite3.OperationalError as e:
        print(e)
    return 'Error when add_log'


def get_logs(request_user_id):
    print('get_logs -> ', request_user_id)
    try:
        db = get_db()
        cur = db.execute('select * from Log where user_id=? order by time desc', (request_user_id,))
        dict_array = json_utils.db_to_json_items(cur)
        for dict_item in dict_array:
            user = auth.find_user(request_id=request_user_id)
            if isinstance(user, dict):
                dict_item['user'] = user
        return dict_array
    except sqlite3.OperationalError as e:
        print(e)
    return 'Error when get_logs'
