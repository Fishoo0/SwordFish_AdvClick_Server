import sqlite3
from time import asctime

from advclick.account.token import Token
from advclick.db.db import get_db


def find_user(user_id, user_name):
    print('find_user user_id -> ' + user_id + ' user_name -> ' + user_name)
    try:
        db = get_db()
        cur = None
        if user_id is not None:
            cur = db.execute('select * from User where name=?', (user_name,))
        elif user_name is not None:
            cur = db.execute('select * from User where id=?', (user_id,))
    except sqlite3.OperationalError:
        print('Can not find user')
    else:
        if cur is not None:
            values = cur.fetchall()
            if len(values) == 1:
                return values[0]
    return None

def register(user_name, user_password):
    if find_user(user_name=user_name) is not None:
        return 'User name has been registered!'
    db = get_db()
    db.execute('insert into User(name,password,time) values (?,?,?)', (user_name, user_password, asctime()))
    db.commit()
    print('User ? has been inserted into db successfully', user_name)
    return None


def login(user_name, user_password=None):
    print("login -> " + user_name)
    item = find_user(user_name=user_name)
    if item is not None:
        password = item[3]
        token = item[4]
        if password == user_password:
            print("password is correct")
            token_obj = Token(item[0], user_name)
            get_db().execute('update User set token=? where name=?', (token_obj.get_token(), user_name))
            get_db().commit()
            print('User has login successfully ,and token has been refreshed')
            return None
        elif password is None or password is '' and token is not None or token is not '':
            print("password is empty ,try to check token")
            token_obj = Token(token=token)
            if token_obj.verify_token():
                print('User has passed token verify!')
                return None
            return 'User ? Token has expired!', user_name
        return 'Password is not correct && token is null!'
    else:
        return 'User has not registered yet, please register first'
    return 'Unknown error'


def logout(user_name):
    get_db().execute('update User set token=? where name=?', (None, user_name))
    get_db().commit()
    print('User ? has logout successfully!', user_name)
    return None
