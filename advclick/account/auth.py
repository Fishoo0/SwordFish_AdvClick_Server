import sqlite3
import time

from advclick.account.token import Token
from advclick.db.db import get_db
from advclick.utils import json_utils


def find_user(request_id=None, request_name=None):
    print('find_user')
    try:
        db = get_db()
        cur = None
        if request_id is not None:
            cur = db.execute('select * from User where id=?', (request_id,))
        elif request_name is not None:
            cur = db.execute('select * from User where name=?', (request_name,))
    except sqlite3.OperationalError as e:
        print(e)
    else:
        if cur is not None:
            values = cur.fetchall()
            if len(values) == 1:
                print('Ok, find user .')
                json_result = json_utils.db_to_json_item(cur, values[0])
                json_result['server_time'] = int(time.time())
                return json_result
            else:
                print('Can not find User !')
        else:
            print('Can not find User!')
    return None


def find_user_id(request_name):
    print('find_user_id' + request_name)
    user = find_user(request_name=request_name)
    if user is not None:
        print('find user id ' + str(user['id']))
        return user['id']
    print('user is None')
    return None;


def register(request_name, request_password, request_im_qq, request_alipay, request_alipay_name):
    if find_user(request_name=request_name) is not None:
        return 'User name has been registered!'
    db = get_db()
    is_admin = 0
    if request_name == 'super_admin':
        is_admin = 1
    db.execute('insert into User(name,password,time,im_qq,alipay,alipay_name,is_admin) values (?,?,?,?,?,?,?)',
               (
                   request_name, request_password, time.asctime(), request_im_qq, request_alipay, request_alipay_name,
                   is_admin))

    # init the click table
    db.execute('insert into Click(time,user_id) values (?,?)',
               (time.asctime(), find_user_id(request_name=request_name)))
    print('User ? has been inserted into db successfully', request_name)
    db.commit()
    return None


def login(request_name, request_password=None):
    print("login -> " + request_name)
    item = find_user(request_name=request_name)
    if item is not None:
        password = item['password']
        token = item['token']
        if password == request_password:
            print("password is correct")
            token_obj = Token(item['id'], request_name)
            get_db().execute('update User set token=? where name=?', (token_obj.get_token(), request_name))
            get_db().commit()
            print('User has login successfully ,and token has been refreshed')
            return None
        elif request_password is None or request_password is '':
            print('request_password is None')
            if token is not None or token is not '':
                print("password is empty ,try to check token")
                token_obj = Token(token=token)
                if token_obj.verify_token():
                    print('User has passed token verify!')
                    return None
                return 'User Token has expired! (' + request_name + ')'
        return 'Password is not correct && token is null!'
    else:
        return 'User has not registered yet, please register first'
    return 'Unknown error'


def logout(request_name):
    get_db().execute('update User set token=? where name=?', (None, request_name))
    get_db().commit()
    print('User ? has logout successfully!', request_name)
    return None


def update_profile(request_id, request_password=None, request_qq=None, request_phone=None,
                   request_alipay=None, request_alipay_name=None, request_prime_level=-1, request_prime_period=-1,
                   request_youmeng_checked=-1):
    print('update_profile')
    db = get_db()
    if request_password is not None and request_password != '':
        print('request_password updated')
        db.execute('update User set password=? where id=?', (request_password, request_id))
    else:
        print('request_password unchanged.')
    if request_qq is not None and request_qq != '':
        print('request_qq updated')
        db.execute('update User set im_qq=? where id=?', (request_qq, request_id))
    else:
        print('request_qq unchanged.')
    if request_phone is not None and request_phone != '':
        print('request_phone updated')
        db.execute('update User set telephone=? where id=?', (request_phone, request_id))
    else:
        print('request_phone unchanged.')

    if request_alipay is not None and request_alipay != '':
        print('request_alipay updated')
        db.execute('update User set alipay=? where id=?', (request_alipay, request_id))
    else:
        print('request_phone unchanged.')
    if request_alipay_name is not None and request_alipay_name != '':
        print('request_alipay_name updated')
        db.execute('update User set alipay_name=? where id=?', (request_alipay_name, request_id))
    else:
        print('request_alipay_name unchanged.')
    if request_prime_level >= 0:
        print('request_prime_level updated')
        db.execute('update User set prime_level=? where id=?', (request_prime_level, request_id))
        db.execute('update User set prime_open_time=? where id=?', (int(time.time()), request_id))  # seconds
        print('prime_update_time is -> ' + str(int(time.time())))
        if request_prime_level == 1:
            if request_prime_period >= 0:
                request_prime_time_end = int((time.time() + request_prime_period));
                print('prime_time_end is -> ' + str(request_prime_time_end))
                db.execute('update User set prime_end_time=? where id=?',
                           (request_prime_time_end, request_id))  # seconds
            else:
                print('User should setup trial time for PrimeTrial!')
    else:
        print('request_prime_level unchanged.')

    if request_youmeng_checked >= 0:
        print('request_youmeng_checked updated')
        db.execute('update User set youmeng_checked=? where id=?', (request_youmeng_checked, request_id))
    else:
        print('request_youmeng_checked unchanged.')

    db.commit()
    return find_user(request_id=request_id)


def check_youmeng(request_id, baidu, google, sougou, taobao):
    print('check_youmeng')
    if baidu is not None and baidu == 'baidu':
        pass
    else:
        return 'Baidu not passed.'
    if google is not None and google == 'google':
        pass
    else:
        return 'Google not passed.'
    if sougou is not None and sougou == 'sougou':
        pass
    else:
        return 'Sougou not passed.'
    if taobao is not None and taobao == 'taobao':
        pass
    else:
        return 'Taobao not passed.'
    db = get_db()
    db.execute('update User set youmeng_checked=? where id=?', (1, request_id))
    db.commit()
    return find_user(request_id=request_id)
