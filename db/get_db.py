import pymysql as pymysql


def get_login_connect():
    connect = pymysql.connect(host='localhost',
                              user='root',
                              password='root',
                              db='login',
                              charset='utf8')
    return connect

