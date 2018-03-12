# -*- coding: utf-8 -*-
from hashlib import sha1
import time
import json
import urllib
import urllib2
import hashlib
import base64
import urllib




def chartime():
    #当前时间戳
    strtime = time.localtime()
    timestamp = time.strftime('%Y%m%d%H%M%S', strtime)
    return  timestamp


#SHA1签名
def design_SHA1(cust_account,org_tempKey,datetime):
    source=cust_account+org_tempKey+datetime
    return sha1(source.encode('utf-8')).hexdigest()




#发送短信
def send_message(app_key,cust_account,org_tempKey,ext_terminalCode,called,msg_id,template_code,template_params):
    url="http://dudu.yonyoutelecom.cn/SMSv4/postSms.do?"
    timestamp=chartime()
    sign=design_SHA1(cust_account,org_tempKey,timestamp)

    datas={
        'app_key':app_key,
        'cust_account':cust_account,
        'timestamp':timestamp,
        'sign': sign,
        'ext_terminalCode': ext_terminalCode,

        'called': called,
        'msg_id':msg_id,
        'template_code':template_code,
        'template_params':template_params,
    }

    """发送post请求"""
    postdata = urllib.urlencode(datas).encode('utf-8')
    print postdata
    header = {
        "Accept": "application/x-www-form-urlencoded;charset=utf-8",
        "Accept-Encoding": "utf-8"
    }
    req = urllib2.Request(url, postdata)
    get_data = urllib2.urlopen(req).read()

    return get_data



