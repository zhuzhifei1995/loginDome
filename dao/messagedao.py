from db import get_db


def insert_message_ship(user_id, friend_id):
    try:
        connect = get_db.get_login_connect()
        cursor = connect.cursor()
        user_ship = get_user_ship_id(user_id, friend_id)
        if len(user_ship) == 0:
            print('insert_message_ship：无关系')
            sql = 'INSERT INTO user_ship (user_id, friend_id) VALUES (' + user_id + ',' + friend_id + ')'
            print('insert_message_ship：' + sql)
            cursor.execute(sql)
            connect.commit()
            connect.close()
        else:
            print('insert_message_ship：有关系')
    except Exception as e:
        print(e)
    return get_user_ship_id(user_id, friend_id)


def get_user_ship_id(user_id, friend_id):
    data = {}
    try:
        connect = get_db.get_login_connect()
        cursor = connect.cursor()
        sql_user_id = 'SELECT * FROM user_ship WHERE user_id = ' + user_id + ' AND friend_id = ' + friend_id
        print('get_user_ship_id：' + sql_user_id)
        cursor.execute(sql_user_id)
        result = cursor.fetchall()
        if len(result) == 0:
            sql_friend_id = 'SELECT * FROM user_ship WHERE user_id = ' + friend_id + ' AND friend_id = ' + user_id
            print('get_user_ship_id：' + sql_friend_id)
            cursor.execute(sql_friend_id)
            result = cursor.fetchall()
        if len(result) > 0:
            for row in result:
                user_ship_id = row[0]
                user_id_result = row[1]
                friend_id_result = row[2]
                data = {
                    "id": user_ship_id,
                    "user_id": user_id_result,
                    "friend_id": friend_id_result,
                }
    except Exception as e:
        print(e)
    return data


def insert_message(user_id, friend_id, create_time, message, message_type):
    try:
        connect = get_db.get_login_connect()
        cursor = connect.cursor()
        user_ship_id = insert_message_ship(user_id, friend_id)['id']
        sql = 'INSERT INTO message (user_ship_id, message,create_time,send_user_id, message_type) ' \
              'VALUES (' + str(user_ship_id) + ',"' + message + '","' + create_time \
              + '",' + user_id + ',' + message_type + ')'
        print(sql)
        cursor.execute(sql)
        connect.commit()
        connect.close()
    except Exception as e:
        print(e)


def get_messages(user_id, friend_id):
    message = []
    try:
        connect = get_db.get_login_connect()
        cursor = connect.cursor()
        user_ship_id = get_user_ship_id(user_id, friend_id)['id']
        sql = 'SELECT * FROM message WHERE user_ship_id = ' + str(user_ship_id)
        print(sql)
        cursor.execute(sql)
        result = cursor.fetchall()
        for row in result:
            message.append({
                'id': row[0],
                'user_ship_id': row[1],
                'message': row[2],
                'create_time': row[3],
                'send_user_id': row[4],
                'message_type': row[5],
            })
    except Exception as e:
        print(e)
    return message
