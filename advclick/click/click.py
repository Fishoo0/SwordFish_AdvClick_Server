import sqlite3

from advclick.account import auth
from advclick.db.db import get_db

def upload_earn(user_id, value):
    print('upload_earn -> ', user_id)
    try:
        db = get_db()
        db.execute('update User set earn_count=? where id=?', (value, user_id,))
        db.commit()
        return None
    except sqlite3.OperationalError:
        print('Can not find user')
    return 'Error when upload_earn!'


def get_earn(user_id):
    print('get_earn -> ', user_id)
    return auth.find_user(user_id=user_id)
