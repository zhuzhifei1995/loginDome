import datetime
import os
import socket
import uuid

from flask import Flask, request

from dao import userdao, messagedao

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.config['UPLOAD_FOLDER_USER_PHOTO'] = 'static/image/user/photo/'
app.config['UPLOAD_FOLDER_USER_MESSAGE'] = 'static/image/message/'
app.config['UPLOAD_FOLDER_VOICE_MESSAGE'] = 'static/voice/message/'


@app.route('/index', methods=['GET', 'POST'])
@app.route('/', methods=['GET', 'POST'])
def index():
    data = {
        'code': '1',
        'status': '服务器启动成功!'
    }
    return data


@app.errorhandler(404)
def error_date(error):
    data = {
        'code': '1',
        'status': '404!'
    }
    print(error)
    return data


@app.route('/register_user', methods=['GET', 'POST'])
def register_user():
    if request.method == 'POST':
        phone = request.form.get("phone")
        password = request.form.get("password")
        photo = request.files.get("file")
        photo_file_name = str(uuid.uuid4()).replace('-', '') + ".png"
        file_path = os.path.join(app.config['UPLOAD_FOLDER_USER_PHOTO']) + photo_file_name
        photo.save(file_path)
        ip = socket.gethostbyname(socket.gethostname())
        create_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        login_number = str(datetime.datetime.now().strftime('%Y%m%d%H%M%S'))
        message = userdao.insert_user(phone, password, create_time, login_number, photo_file_name)
        if message['code'] == '1':
            data = {
                'code': message['code'],
                'status': message['status'],
                'message': {
                    'phone': phone,
                    'password': password,
                    'photo_url': "http://" + ip + ":8080/static/image/user/photo/" + photo_file_name,
                    'nick_name': '',
                    'create_time': create_time,
                    'login_number': login_number,
                }
            }
        else:
            data = {
                'code': message['code'],
                'status': message['status'],
                'phone': phone
            }
    else:
        data = {
            'code': '0', 'status':
                '注册失败，不支持的请求，请重试！'
        }
    print(data)
    return data


@app.route('/query_user_by_phone', methods=['GET', 'POST'])
def query_user_by_phone():
    if request.method == 'POST':
        phone = request.form.get('phone')
        user = userdao.query_user_by_phone(phone)
        if user != {}:
            ip = socket.gethostbyname(socket.gethostname())
            data = {
                'code': '1',
                'status': '获取查找的手机号用户成功！',
                'message': {
                    'id': user['id'],
                    'phone': phone,
                    'password': user['password'],
                    'photo': "http://" + ip + ":8080/static/image/user/photo/" + user['photo_url'],
                    'nick_name': user['nick_name'],
                    'create_time': user['create_time'],
                    'login_number': user['login_number'],
                }
            }
        else:
            data = {
                'code': '0',
                'status': '当前手机号未注册用户！',
            }
    else:
        data = {
            'code': '0',
            'status': '获取失败，不支持的请求，请重试！'
        }
    print(data)
    return data


@app.route('/query_all_user', methods=['GET', 'POST'])
def query_all_user():
    if request.method == 'POST':
        user_id = request.form.get("id")
        try:
            users = userdao.query_all_user(user_id)
            data = {
                'code': '1',
                'status': '获取所有好友成功！',
                'message': users
            }
        except KeyError as e:
            print(e)
            data = {
                'code': '0',
                'status': '获取失败，当前没有好友！！',
            }
    else:
        data = {
            'code': '0',
            'status': '获取失败，不支持的请求，请重试！'
        }
    print(data)
    return data


@app.route('/query_user_by_id', methods=['GET', 'POST'])
def query_user_by_id():
    if request.method == 'POST':
        user_id = request.form.get("id")
        user = userdao.query_user_by_id(user_id)
        ip = socket.gethostbyname(socket.gethostname())
        data = {
            'code': '1',
            'status': '获取用户信息成功！',
            'message': {
                'id': user['id'],
                'phone': user['phone'],
                'password': user['password'],
                'photo_url': "http://" + ip + ":8080/static/image/user/photo/" + user['photo'],
                'nick_name': user['nick_name'],
                'create_time': user['create_time'],
                'login_number': user['login_number'],
                'android_id': user['android_id']
            }
        }
    else:
        data = {
            'code': '0',
            'status': '查询失败，不支持的请求，请重试！'
        }
    print(data)
    return data


@app.route('/update_user_photo', methods=['GET', 'POST'])
def update_user_photo():
    if request.method == 'POST':
        user_id = request.form.get("id")
        user = userdao.query_user_by_id(user_id)
        photo = request.files.get("file")
        try:
            photo_file_name = user['photo']
            file_path = os.path.join(app.config['UPLOAD_FOLDER_USER_PHOTO']) + photo_file_name
            photo.save(file_path)
            data = {
                'code': 1,
                'status': '修改头像成功！',
                'message': user
            }
        except KeyError as e:
            print(e)
            data = {
                'code': '0',
                'status': '修改头像失败，用户不存在，请重新登录！！'
            }
    else:
        data = {
            'code': '0',
            'status': '修改头像失败，不支持的请求，请重试！'
        }
    print(data)
    return data


@app.route('/update_user_nike_name_by_id', methods=['GET', 'POST'])
def update_user_nike_name_by_id():
    if request.method == 'POST':
        user_id = request.form.get("user_id")
        nick_name = request.form.get("nick_name")
        status = userdao.update_user_nike_name_by_id(user_id, nick_name)
        if status == 1:
            data = {
                'code': '1',
                'status': '修改昵称成功！',
                'nick_name': nick_name
            }
        elif status == 0:
            data = {
                'code': '0',
                'status': '用户不存在，修改失败，请重试！'
            }
        else:
            data = {
                'code': '0',
                'status': '操作数据库失败，修改失败，请重试！'
            }
    else:
        data = {
            'code': '0',
            'status': '修改失败，不支持的请求，请重试！'
        }
    print(data)
    return data


@app.route('/update_phone_by_id', methods=['GET', 'POST'])
def update_phone_by_id():
    if request.method == 'POST':
        user_id = request.form.get("user_id")
        phone = request.form.get("phone")
        status = userdao.update_phone_by_id(user_id, phone)
        if status == 1:
            data = {
                'code': '1',
                'status': '修改绑定的手机号成功！',
                'password': phone
            }
        elif status == 0:
            data = {
                'code': '0',
                'status': '用户不存在，修改失败，请重试！'
            }
        else:
            data = {
                'code': '0',
                'status': '操作数据库失败，修改失败，请重试！'
            }
    else:
        data = {
            'code': '0',
            'status': '修改失败，不支持的请求，请重试！'
        }
    print(data)
    return data


@app.route('/update_password_by_id', methods=['GET', 'POST'])
def update_password_by_id():
    if request.method == 'POST':
        user_id = request.form.get("user_id")
        password = request.form.get("password")
        status = userdao.update_password_by_id(user_id, password)
        if status == 1:
            data = {
                'code': '1',
                'status': '修改密码成功！',
                'password': password
            }
        elif status == 0:
            data = {
                'code': '0',
                'status': '用户不存在，修改失败，请重试！'
            }
        else:
            data = {
                'code': '0',
                'status': '操作数据库失败，修改失败，请重试！'
            }
    else:
        data = {
            'code': '0',
            'status': '修改失败，不支持的请求，请重试！'
        }
    print(data)
    return data


@app.route('/login_user', methods=['GET', 'POST'])
def login_user():
    if request.method == 'POST':
        login_number = request.form.get("login_number")
        password = request.form.get("password")
        android_id = request.form.get("android_id")
        user = userdao.query_user_by_login_number(login_number)
        if user == {}:
            data = {
                'code': '0',
                'status': '登陆失败，该用户不存在！',
                'login_number': login_number
            }
        else:
            if password == user['password']:
                userdao.update_android_id_by_id(str(user['id']), android_id)
                data = {
                    'code': '1',
                    'status': '登陆成功！',
                    "message": user
                }
            else:
                data = {
                    'code': '0',
                    'status': '登陆失败，用户登陆密码错误！',
                    'login_number': login_number,
                    'password': password
                }
    else:
        data = {
            'code': '0',
            'status': '登陆失败，不支持的请求，请重试！'
        }
    print(data)
    return data


@app.route('/send_message', methods=['GET', 'POST'])
def send_message():
    if request.method == 'POST':
        user_id = request.form.get('user_id')
        friend_id = request.form.get('friend_id')
        message_type = request.form.get('message_type')
        create_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if message_type == '1':
            message = request.form.get('message')
        elif message_type == '2':
            photo = request.files.get("file")
            message = request.form.get('message') + ".png"
            file_path = os.path.join(app.config['UPLOAD_FOLDER_USER_MESSAGE']) + message
            photo.save(file_path)
        else:
            photo = request.files.get("file")
            message = request.form.get('message') + ".amr"
            file_path = os.path.join(app.config['UPLOAD_FOLDER_VOICE_MESSAGE']) + message
            photo.save(file_path)
        messagedao.insert_message(str(user_id), str(friend_id), create_time, message, message_type)
        data = {
            'code': '1',
            'status': '消息发送成功！'
        }
    else:
        data = {
            'code': '0',
            'status': '消息发送失败，不支持的请求，请重试！'
        }
    print(data)
    return data


@app.route('/get_messages', methods=['GET', 'POST'])
def get_messages():
    if request.method == 'POST':
        message_data = []
        user_id = request.form.get('user_id')
        friend_id = request.form.get('friend_id')
        messages = messagedao.get_messages(str(user_id), str(friend_id))
        ip = socket.gethostbyname(socket.gethostname())
        for message in messages:
            if user_id == str(message['send_user_id']):
                send_code = 1
            else:
                send_code = 0
            if str(message['message_type']) == '1':
                message_data.append({
                    'id': message['id'],
                    'user_ship_id': message['user_ship_id'],
                    'message': message['message'],
                    'create_time': str(message['create_time']),
                    'send_code': send_code,
                    'message_type': str(message['message_type']),
                })
            elif str(message['message_type']) == '2':
                message_data.append({
                    'id': message['id'],
                    'user_ship_id': message['user_ship_id'],
                    'message': message['message'],
                    'message_image_url': "http://" + ip + ":8080/static/image/message/" + message['message'],
                    'create_time': str(message['create_time']),
                    'send_code': send_code,
                    'message_type': str(message['message_type']),
                })
            elif str(message['message_type']) == '3':
                message_data.append({
                    'id': message['id'],
                    'user_ship_id': message['user_ship_id'],
                    'message': message['message'],
                    'message_voice_url': "http://" + ip + ":8080/static/voice/message/" + message['message'],
                    'create_time': str(message['create_time']),
                    'send_code': send_code,
                    'message_type': str(message['message_type']),
                })
        data = {
            'code': '1',
            'status': '获取所有消息成功！',
            "message": message_data
        }
    else:
        data = {
            'code': '0',
            'status': '消息发送失败，不支持的请求，请重试！'
        }
    print(data)
    return data


@app.route('/phone_is_register_user', methods=['GET', 'POST'])
def phone_is_register_user():
    if request.method == 'POST':
        phone = request.form.get("phone")
        user = userdao.query_user_by_phone(phone)
        if user == {}:
            data = {
                'code': '1',
                'status': '验证成功，该手机号可以注册！',
                'phone': phone,
                'verification_code': userdao.get_verification_code(),
            }
        else:
            ip = socket.gethostbyname(socket.gethostname())
            data = {
                'code': '0',
                'status': '注册失败，该手机号已注册过账号，请直接登陆！',
                'message': {
                    'id': user['id'],
                    'phone': phone,
                    'password': user['password'],
                    'photo_url': "http://" + ip + ":8080/static/image/user/photo/" + user['photo_url'],
                    'nick_name': user['nick_name'],
                    'create_time': user['create_time'],
                    'login_number': user['login_number'],
                }
            }
    else:
        data = {
            'code': '0',
            'status': '登陆失败，不支持的请求，请重试！'
        }
    print(data)
    return data


if __name__ == '__main__':
    print(socket.gethostbyname(socket.gethostname()))
    app.run(debug=True, host='0.0.0.0', port=8080)
