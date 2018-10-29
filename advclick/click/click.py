import sqlite3
from time import asctime

from advclick.db.db import get_db
from advclick.utils import json_utils


# Not safe, should be https or some encryption
def upload_earn(request_user_id, request_value):
    print('upload_earn -> ' + request_user_id + ' request_value -> ' + str(request_value))
    try:
        db = get_db()

        cur = db.execute('select * from Click where user_id=?', (request_user_id,))
        value = cur.fetchall()
        if len(value) == 1:
            current_earn_amount = value[0][3]
            print('Current earn_amount is ' + str(current_earn_amount))
            db.execute('update Click set earn_amount=? where user_id=?',
                       (float(request_value + current_earn_amount), request_user_id,))
            db.commit()
        else:
            print('Can not find user !')
            return None
    except sqlite3.OperationalError as e:
        print(e)
        return None
    return get_earn(request_user_id)


def get_earn(request_user_id, to_dict=True):
    print('get_earn -> ', request_user_id)
    try:
        db = get_db()
        cur = None
        if request_user_id is not None:
            cur = db.execute('select * from Click where user_id=?', (request_user_id,))
    except sqlite3.OperationalError as e:
        print(e)
    else:
        if cur is not None:
            values = cur.fetchall()
            if len(values) == 1:
                if to_dict:
                    return json_utils.db_to_json_item(cur, values[0])
                else:
                    return values[0]
            else:
                print('values is not 1 ??')
    return None


def request_withdraw(request_user_id, value=0.0):
    print('request_withdraw')
    try:
        db = get_db()
        cur = db.execute('select * from Click where user_id=?', (request_user_id,))
        items = cur.fetchall()
        if len(items) == 1:
            print('Ok, find withdraw info ...')
            item = items[0]

            earn_amount = item[3]
            with_draw_time_left = item[4]
            print('earn_amount -> ' + str(earn_amount) + ' with_draw_time_left -> ' + str(with_draw_time_left))

            if with_draw_time_left < 1:
                print('You have no with_draw time left.')
                return 'You have no with_draw time left.'

            # just set it to total temp
            if value <= 0 or value > earn_amount:
                value = earn_amount

            if with_draw_time_left > 0:
                print('request value is ' + str(value))
                db.execute('update Click set request_with_draw_amount=? where user_id=?', (value, request_user_id,))
                db.execute('update Click set request_with_draw_time=? where user_id=?', (asctime(), request_user_id,))
                db.execute('update Click set with_draw_times_left=? where user_id=?',
                           ((with_draw_time_left - 1), request_user_id,))
                db.commit()
                return get_earn(request_user_id)
            else:
                print('You have no withdraw time left.')
                return 'You have no withdraw time left.'
        else:
            print('You have not earned anything.')
    except sqlite3.OperationalError as e:
        print(e)
    return 'Error when upload_earn!'


# Not safe, should be https or some encryption
def update_click(request_user_id, request_earn_amount=-1, request_with_draw_times_left=-1,
                 request_request_with_draw_amount=-1):
    print('update_click')
    try:
        db = get_db()
        if request_earn_amount >= 0:
            print('earn_amount updated')
            db.execute('update Click set earn_amount=? where user_id=?',
                       (request_earn_amount, request_user_id,))
        else:
            print('earn_amount unchanged')

        if request_with_draw_times_left >= 0:
            print('with_draw_times_left updated')
            db.execute('update Click set with_draw_times_left=? where user_id=?',
                       (request_with_draw_times_left, request_user_id,))
        else:
            print('with_draw_times_left unchanged')

        if request_request_with_draw_amount >= 0:
            print('request_with_draw_amount updated')
            db.execute('update Click set request_with_draw_amount=? where user_id=?',
                       (request_request_with_draw_amount, request_user_id,))
        else:
            print('request_with_draw_amount unchanged')

        db.execute('update Click set manager_deal_time=? where user_id=?',
                   (asctime(), request_user_id,))
        db.commit()
    except sqlite3.OperationalError as e:
        print(e)
        return 'db error !'
    return get_earn(request_user_id)


# Not safe, should be https or some encryption
def onekey_withdraw(request_user_id):
    print('onekey_withdraw')
    earn = get_earn(request_user_id=request_user_id, to_dict=False)
    if earn is not None:
        current_earn_amount = earn[3]
        current_with_draw_times_left = earn[4]
        current_request_with_draw_amount = earn[5]
        print('current_earn_amount -> ' + str(current_earn_amount))
        print('current_request_with_draw_amount -> ' + str(current_request_with_draw_amount))
        print('current_with_draw_times_left -> ' + str(current_with_draw_times_left))

        if current_earn_amount > 0:
            if current_request_with_draw_amount > 0:
                if current_with_draw_times_left >= 1:
                    if current_request_with_draw_amount > current_earn_amount:
                        request_request_with_draw_amount = current_request_with_draw_amount - current_earn_amount
                    else:
                        request_request_with_draw_amount = 0
                    request_earn_amount = current_earn_amount - (
                        current_request_with_draw_amount - request_request_with_draw_amount)
                    request_with_draw_times_left = current_with_draw_times_left - 1
                    return update_click(request_user_id, request_earn_amount, request_with_draw_times_left,
                                        request_request_with_draw_amount)
                else:
                    return 'You have no withdraw times left.'
            else:
                return 'You have no any withdraw amount left.'
        else:
            return 'You have no earn amount left.'
    return 'Can not find such user.'
