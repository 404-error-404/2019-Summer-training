# -*- coding:utf-8 -*-
import pymysql
import json

connection = pymysql.connect(
    "47.107.226.69",    # hoost ip地址
    "wangrenjie",       # port 端口，mysql默认为3306
    "123456789",        # user 用户
    "training"          # db 数据库名称
)
# 使用cursor()方法获取操作游标
cursor = connection.cursor()
# 关闭数据库连接
connection.close()

# 注册账号是写入数据库
def signup(email, password, nickname, avatar_address, usertype):
    sql = 'insert into user (username, avatar_address, id, password, usertype)' \
          ' values("%s", "%s", "%s", "%s", "%s")' %(nickname, avatar_address, email, password, usertype)
    try:
        # 连接数据库
        connection.connect()
        # 执行SQL语句
        cursor.execute(sql)
        connection.commit()
        # 关闭数据库连接
        connection.close()
        return True
    except Exception as e:
        connection.close()
        return e

# 从数据库中查找指定邮箱对应的密码
def search_password(email):
    sql = 'select password, username, usertype from user where id = "%s"' %email
    try:
        # 连接数据库
        connection.connect()
        # 执行SQL语句
        cursor.execute(sql)
        # connection.commit() 查询操作不需要这一句，但是插入等需要
        results = cursor.fetchall()
        pyjson = {}
        pyjson["statusCode"] = 0
        pyjson["password"] = None
        for row in results:
            pyjson["password"] = row[0]
            pyjson["username"] = row[1]
            pyjson["usertype"] = row[2]
        # 关闭数据库连接
        connection.close()
        pyjson_str = json.dumps(pyjson, ensure_ascii=False)
        return pyjson_str
    except Exception as e:
        connection.close()
        pyjson = {}
        pyjson["statusCode"] = -1
        pyjson["errorDetail"] = "数据库查询出错了"
        pyjson_str = json.dumps(pyjson, ensure_ascii=False)
        return pyjson_str

# 更新指定邮箱的密码
def update_password(email, new_password):
    sql = 'update user set password = %s where id = "%s"' %(new_password, email)
    try:
        # 连接数据库
        connection.connect()
        # 执行SQL语句
        cursor.execute(sql)
        connection.commit() #查询操作不需要这一句，但是插入等需要
        # 关闭数据库连接
        connection.close()
        return True
    except Exception as e:
        connection.close()
        return False

# 登录时查询用户昵称和用户类型
def select_username_and_usertype(email):
    sql = 'select username, usertype from user where id = "%s"' %email
    try:
        # 连接数据库
        connection.connect()
        # 执行SQL语句
        cursor.execute(sql)
        # connection.commit() 查询操作不需要这一句，但是插入等需要
        results = cursor.fetchall()
        for row in results:
            username = row[0]
            usertype = row[1]
        # 关闭数据库连接
        connection.close()
        pyjson = {}
        pyjson["statuscodde"] = 0
        pyjson["username"] = username
        pyjson["usertype"] = usertype
        pyjson_str = json.dumps(pyjson, ensure_ascii=False)
        return pyjson_str
    except Exception as e:
        connection.close()
        pyjson = {}
        pyjson["statuscodde"] = 1
        pyjson_str = json.dumps(pyjson, ensure_ascii=False)
        return pyjson_str