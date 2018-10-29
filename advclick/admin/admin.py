import sqlite3
import time

from advclick.account import auth
from advclick.db.db import get_db


def find_users(request_user_id):
    print('find_users user_id -> ' + request_user_id)
    if check_admin(request_user_id=request_user_id):
        try:
            db = get_db()
            cursor = db.execute('select * from User')
            row_headers = [key[0] for key in cursor.description]
            json_data = []
            items = cursor.fetchall()
            for item in items:
                item_dict = dict(zip(row_headers, item))
                item_dict['server_time'] = int(time.time())
                json_data.append(item_dict)
            return json_data
        except sqlite3.OperationalError as e:
            print(e)
    else:
        return 'Permission denied !'
    return None


def check_admin(request_user_id):
    user = auth.find_user(request_id=request_user_id)
    if user is not None:
        admin_name = user['name']
        if admin_name == 'super_admin':
            return True
    return False
