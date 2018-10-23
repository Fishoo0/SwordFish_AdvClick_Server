import sqlite3
from time import asctime

from advclick.account.token import Token
from advclick.click import click
from advclick.db.db import get_db
from advclick.utils import json_utils


def find_user(request_id=None, request_name=None, to_dict=False):
    try:
        db = get_db()
        cur = None
        if request_id is not None:
            cur = db.execute('select * from User where id=?', (request_id,))
        elif request_name is not None:
            cur = db.execute('select * from User where name=?', (request_name,))
    except sqlite3.OperationalError:
        print('Can not find user')
    else:
        if cur is not None:
            values = cur.fetchall()
            if len(values) == 1:
                if to_dict:
                    return json_utils.db_to_json_item(cur, values[0])
                else:
                    return values[0]
    return None


def find_user_id(request_name):
    print('find_user_id' + request_name)
    user = find_user(request_name=request_name)
    if user is not None:
        print('find user id ' + str(user[0]))
        return user[0]
    print('user is None')
    return None;


def register(request_name, request_password, request_im_qq, request_alipay, request_alipay_name):
    if find_user(request_name=request_name) is not None:
        return 'User name has been registered!'
    db = get_db()
    db.execute('insert into User(name,password,time,im_qq,alipay,alipay_name) values (?,?,?,?,?,?)',
               (request_name, request_password, asctime(), request_im_qq, request_alipay, request_alipay_name))
    db.commit()

    # init the click table
    db.execute('insert into Click(time,user_id) values (?,?)',
               (asctime(), find_user_id(request_name=request_name)))
    print('User ? has been inserted into db successfully', request_name)
    db.commit()
    return None


def login(request_name, request_password=None):
    print("login -> " + request_name)
    item = find_user(request_name=request_name)
    if item is not None:
        password = item[3]
        token = item[4]
        if password == request_password:
            print("password is correct")
            token_obj = Token(item[0], request_name)
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
                return 'User ? Token has expired!', request_name
        return 'Password is not correct && token is null!'
    else:
        return 'User has not registered yet, please register first'
    return 'Unknown error'


def logout(request_name):
    get_db().execute('update User set token=? where name=?', (None, request_name))
    get_db().commit()
    print('User ? has logout successfully!', request_name)
    return None
