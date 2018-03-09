#!/usr/local/bin/python
# -*- coding:utf-8 -*-
# Author: jacky
# Time: 14-2-22 下午11:48
# Desc: 短信http接口的python代码调用示例
import httplib
import urllib
import json

# 请求地址请登录253云通讯自助通平台查看或者询问您的商务负责人获取

host = "smssh1.253.com"
# host = "smsbj1.253.com"
# 端口号
port = 80
# 版本号
version = "v1.1"
# 智能匹配模版短信接口的URI
# sms_send_uri = "/msg/send/json"
sms_send_uri = "/msg/variable/json"
# 创蓝账号
account = "N6477034"
# account = "M3631337"
# 创蓝密码
password = "Hry7eSAjXa66bd"
# password = "3ZDKAGF6yqea87"
params = "13578503881,989990;"
text = "【253云通讯】您好！验证码是：{$var}，短信有效时间为2分钟。"
tt = {'account': account, 'password': password, 'msg': text, 'params': params}
tt = json.dumps(tt)
# print urllib.quote('编码坑爹')
# print urllib.quote('编码坑爹'.decode('gbk').encode('utf-8'))
headers = {"Content-type": "application/json"}
conn = httplib.HTTPConnection("smssh1.253.com", port=80, timeout=30)
conn.request("POST", "/msg/variable/json", tt, headers)
response = conn.getresponse()
response_str = response.read()
conn.close()
print response_str


