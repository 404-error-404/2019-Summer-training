# -*- coding:utf-8 -*-
from os import path

from app01.function.mysql import *
from django.http import HttpResponse
from app01.function.mail import mail

import json

# Create your views here.

def responseTest(request):
    return HttpResponse("测试成功")

def movie(request):
    return HttpResponse("优酷电影首页")

def movie_detial(request, movie_id):
    return HttpResponse("正在播放编号为：%s电影" % movie_id)

def login(request):  # 登录
    email = request.GET.get('email')
    password = request.GET.get('password')
    # 查询user的密码是否和输入匹配————查询数据库操作
    json_result = search_password(email)
    result = json.loads(json_result)
    if(result["statusCode"] == 0):
        if(result["password"] == None):
            json_result = {}
            json_result["statusCode"] = 1
            json_result["errorDetail"] = "亲，您还未注册哦"
            json_result = json.dumps(json_result, ensure_ascii=False)
        elif(password == result["password"]):
            result.pop('password')
        else:
            json_result = {}
            json_result["statusCode"] = 2
            json_result["errorDetail"] = "亲，密码不对哦"
            json_result = json.dumps(json_result, ensure_ascii=False)
    return HttpResponse(json_result)

def register_code(request):   #注册时或者找回密码的时候获取验证码
    receiver = request.GET.get('email')  # 收件人邮箱账号，我这边发送给自己
    verification_code = mail(receiver)
    return HttpResponse(verification_code)

def register(request):  # 注册账户
    username = request.GET.get('user')
    password = request.GET.get('password')
    email = request.GET.get('email')
    avatar_address = 'noAvatar'
    account_type = 'student'
    # 把新账号写入数据库————写入数据库操作
    result = signup(email, password, username, avatar_address, account_type)
    print(result)
    return HttpResponse(result)

def change_password(request):  # 修改密码
    email = request.GET.get('email')
    old_password = request.GET.get('old_password')
    new_password = request.GET.get('new_password')
    # 检查旧的密码是否相同————查询数据库操作
    now_password = search_password(email)
    if(now_password == None):
        return HttpResponse("此账户不存在，请核对账户")
    elif(now_password == False):
        return HttpResponse("某个地方出错了，程序员小哥哥正在努力解决")
    elif(now_password == old_password):
        # 更新用户密码————更改数据库操作
        update_password_result = update_password(email, new_password)
        return HttpResponse(update_password_result)
    else:
        return HttpResponse("密码不正确，请仔细核对")

def show_image(request,news_id):
    d = path.dirname(__file__)
    #parent_path = path.dirname(d)
    print("d="+str(d))
    imagepath = path.join(d,"static/show/wordimage/"+str(news_id)+".png")
    print("imagepath="+str(imagepath))
    image_data = open(imagepath,"rb").read()
    return HttpResponse(image_data,content_type="image/png") #注意旧版的资料使用mimetype,现在已经改为content_type
