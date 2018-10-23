import sqlite3
from time import asctime

from advclick.db.db import get_db
from advclick.utils import json_utils


# Not safe, should be https or some encryption
def upload_earn(request_user_id, value=0):
    print('upload_earn -> ', request_user_id)
    try:
        db = get_db()
        db.execute('update Click set earn_count=? where user_id=?', (value, request_user_id,))
        db.commit()
        return None
    except sqlite3.OperationalError:
        print('Can not find user')
    return 'Error when upload_earn!'


def get_earn(request_user_id):
    print('get_earn -> ', request_user_id)
    try:
        db = get_db()
        cur = None
        if request_user_id is not None:
            cur = db.execute('select * from Click where user_id=?', (request_user_id,))
    except sqlite3.OperationalError:
        print('Can not find user')
    else:
        if cur is not None:
            values = cur.fetchall()
            if len(values) == 1:
                return json_utils.db_to_json_item(cur, values[0])
            else:
                print('values is not 1??')
    return None


def request_withdraw(request_user_id, value=0.0):
    print('request_withdraw')
    try:
        db = get_db()
        if value == 0:
            print('value is none, figure from db ...')
            cur = db.execute('select earn_amount from Click where user_id=?', (request_user_id,))
            items = cur.fetchall()
            if len(items) == 1:
                item = items[0]
            value = item[0]
            if value == 0:
                print('can not figure withdraw amount or earn_amount is 0')
                return 'can not figure withdraw amount or earn_amount is 0'

        print('request value is ' + str(value))
        db.execute('update Click set request_with_draw_amount=? where user_id=?', (value, request_user_id,))
        db.execute('update Click set request_with_draw_time=? where user_id=?', (asctime(), request_user_id,))
        db.commit()
        return None
    except sqlite3.OperationalError:
        print('Can not find user')
    return 'Error when upload_earn!'
