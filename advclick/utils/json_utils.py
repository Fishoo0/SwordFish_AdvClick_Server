import json


def cursor_to_json(sql_result):
    items = []


def cursor_to_json2(cur):
    row_headers = [x[0] for x in cur.description]  # this will extract row headers
    rv = cur.fetchall()

    json_data = []

    for result in rv:
        json_data.append(dict(zip(row_headers, result)))
    return json.dumps(json_data)


def db_to_json_item(cursor, item):
    row_headers = [key[0] for key in cursor.description]
    dict_result = dict(zip(row_headers, item))
    return dict_result


def db_to_json_items(cursor):
    row_headers = [key[0] for key in cursor.description]
    json_data = []
    items = cursor.fetchall()
    for item in items:
        json_data.append(dict(zip(row_headers, item)))
    return json_data
