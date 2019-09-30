#coding:utf-8
__author__ = 'zy'
import urllib2
import cookielib
import urllib
import requests
import re
import sys
'''模拟登录'''
CaptchaUrl = "http://210.42.121.241//servlet/GenImg"
PostUrl = "http://210.42.121.241/servlet/Login"
# 验证码地址和post地址
cookie = cookielib.CookieJar()
handler = urllib2.HTTPCookieProcessor(cookie)
opener = urllib2.build_opener(handler)
# 将cookies绑定到一个opener cookie由cookielib自动管理
username = '2017302580112'
password = '19990113'
# 用户名和密码
picture = opener.open(CaptchaUrl).read()
# 用openr访问验证码地址,获取cookie
local = open('e:/image.jpg', 'wb')
local.write(picture)
local.close()
# 保存验证码到本地
SecretCode = raw_input('输入验证码： ')
# 打开保存的验证码图片 输入
postData = {
'id': username,
'pwd': password,
'xdvfb': SecretCode,
}
# 根据抓包信息 构造表单
headers = {
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
'Accept-Encoding':'gzip, deflate',
'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
'Cache-Control':'max-age=0',
'Connection': 'keep-alive',
'Content-Length':'64',
'Content-Type': 'application/x-www-form-urlencoded',
'Host':'210.42.121.241',
'Origin':'http://210.42.121.241',
'Cookie':cookie,
'Referer':'http://210.42.121.241/',
#'Upgrade-Insecure-Requests':1,
'User-Agent': 'User-Agent:Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.59 Safari/537.36',
}
# 根据抓包信息 构造headers
data = urllib.urlencode(postData)
# 生成post数据 ?key1=value1&key2=value2的形式
request = urllib2.Request(PostUrl, data, headers)
# 构造request请求
#try:
response = opener.open(request)
result = response.read().decode('gb2312')

# 由于该网页是gb2312的编码，所以需要解码
print(result)
    # 打印登录后的页面
#except (urllib2.HTTPError),e:
#    print e.code66
# 利用之前存有cookie的opener登录页面
