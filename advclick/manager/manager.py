import sqlite3

from advclick.db.db import get_db


def find_users(user_id):
    print('find_users user_id -> ' + user_id)
    try:
        db = get_db()
        cur = db.execute('select * from User')
    except sqlite3.OperationalError:
        print('Can not find user')
    else:
        values = cur.fetchall()
        if len(values) > 0:
            return values
    return None


def upload_with_draw_times(owner_id, user_id, times):
    print('upload_with_draw_times owner_id -> ' + owner_id + ' user_id -> ' + user_id + ' times -> ' + times)
    try:
        db = get_db()
        cur = db.execute('update User set times=? where id=?', (times, user_id,))
        db.commit()
    except sqlite3.OperationalError:
        print('Can not find user')
    else:
        values = cur.fetchall()
        if len(values) == 1:
            return values[0]
