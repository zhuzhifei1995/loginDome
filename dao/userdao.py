import random
import socket

from db import get_db


def insert_user(phone, password, create_time, login_number, photo_url):
    connect = get_db.get_login_connect()
    try:
        cursor = connect.cursor()
        sql = 'INSERT INTO `user`' \
              '(phone, password, create_time, login_number, photo_url) VALUES' \
              '("' + phone + '","' \
              + password + '","' \
              + create_time + '","' \
              + login_number + '","' \
              + photo_url + '")'
        print(sql)
        cursor.execute(sql)
        connect.commit()
        connect.close()
        data = {
            'code': '1',
            'status': '注册成功！'
        }
    except Exception as e:
        print(e)
        connect.rollback()
        connect.close()
        data = {
            'code': '0',
            'status': '操作数据库失败，请重试！'
        }
    return data


def query_user_by_login_number(login_number):
    user = {}
    connect = get_db.get_login_connect()
    try:
        cursor = connect.cursor()
        sql = 'SELECT * FROM `user`' \
              ' WHERE login_number = "' + login_number + '"'
        ip = socket.gethostbyname(socket.gethostname())
        cursor.execute(sql)
        results = cursor.fetchall()
        for row in results:
            user_id = row[0]
            nick_name = row[1]
            password = row[2]
            create_time = row[3]
            photo = row[4]
            phone = row[5]
            user = {'id': user_id,
                    'nick_name': nick_name,
                    'password': password,
                    'create_time': str(create_time),
                    'photo': "http://" + ip + ":8080/static/image/user/photo/" + photo,
                    'phone': phone,
                    'login_number': login_number,
                    }
        return user
    except Exception as e:
        print(e)
        return user


def update_user_nike_name_by_id(user_id, nick_name):
    connect = get_db.get_login_connect()
    try:
        cursor = connect.cursor()
        sql = 'UPDATE `user` SET nick_name = "' + nick_name + '" WHERE id =' + user_id
        print(sql)
        status = cursor.execute(sql)
        connect.commit()
        connect.close()
        if status == 1:
            return 1
        else:
            return 0
    except Exception as e:
        connect.rollback()
        connect.close()
        print(e)
        return -1


def update_password_by_id(user_id, password):
    connect = get_db.get_login_connect()
    try:
        cursor = connect.cursor()
        sql = 'UPDATE `user` SET password = "' + password + '" WHERE id =' + user_id
        print(sql)
        status = cursor.execute(sql)
        connect.commit()
        connect.close()
        if status == 1:
            return 1
        else:
            return 0
    except Exception as e:
        connect.rollback()
        connect.close()
        print(e)
        return -1


def update_phone_by_id(user_id, phone):
    connect = get_db.get_login_connect()
    try:
        cursor = connect.cursor()
        sql = 'UPDATE `user` SET phone = "' + phone + '" WHERE id =' + user_id
        print(sql)
        status = cursor.execute(sql)
        connect.commit()
        connect.close()
        if status == 1:
            return 1
        else:
            return 0
    except Exception as e:
        connect.rollback()
        connect.close()
        print(e)
        return -1


def query_user_by_id(user_id):
    user = {}
    connect = get_db.get_login_connect()
    try:
        cursor = connect.cursor()
        sql = 'SELECT * FROM `user`' \
              ' WHERE id = ' + user_id
        cursor.execute(sql)
        results = cursor.fetchall()
        for row in results:
            nick_name = row[1]
            password = row[2]
            create_time = row[3]
            photo = row[4]
            phone = row[5]
            login_number = row[6]
            user = {
                'id': str(user_id),
                'nick_name': nick_name,
                'password': password,
                'create_time': str(create_time),
                'photo': photo,
                'phone': phone,
                'login_number': login_number,
            }
        return user
    except Exception as e:
        print(e)
        return user


def query_all_user(user_id):
    users = []
    connect = get_db.get_login_connect()
    try:
        cursor = connect.cursor()
        sql = 'SELECT * FROM `user`'
        ip = socket.gethostbyname(socket.gethostname())
        cursor.execute(sql)
        results = cursor.fetchall()
        for row in results:
            user__id = str(row[0])
            if user__id != user_id:
                nick_name = row[1]
                password = row[2]
                create_time = row[3]
                photo = row[4]
                phone = row[5]
                login_number = row[6]
                user = {
                    'id': str(user__id),
                    'nick_name': nick_name,
                    'password': password,
                    'create_time': str(create_time),
                    'photo': "http://" + ip + ":8080/static/image/user/photo/" + photo,
                    'phone': phone,
                    'login_number': login_number,
                }
                users.append(user)
        return users
    except Exception as e:
        print(e)
        return users


def query_user_by_phone(phone):
    user = {}
    connect = get_db.get_login_connect()
    try:
        cursor = connect.cursor()
        sql = 'SELECT * FROM `user`' \
              ' WHERE phone = "' + phone + '"'
        cursor.execute(sql)
        results = cursor.fetchall()
        for row in results:
            user_id = row[0]
            nick_name = row[1]
            password = row[2]
            create_time = row[3]
            photo_url = row[4]
            login_number = row[6]
            user = {
                'id': user_id,
                'nick_name': nick_name,
                'password': password,
                'create_time': str(create_time),
                'photo_url': photo_url,
                'phone': phone,
                'login_number': login_number,
            }
        return user
    except Exception as e:
        print(e)
        return user


def get_verification_code():
    verification_code = ''
    for i in range(6):
        ch = chr(random.randrange(ord('0'), ord('9') + 1))
        verification_code += ch
    return verification_code
