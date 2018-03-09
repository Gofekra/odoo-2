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

"""发送post请求"""
def send_post(url,datas):
    header = {
        "Accept": "application/x-www-form-urlencoded;charset=utf-8",
        "Accept-Encoding": "utf-8"
    }

    postdata = urllib.urlencode(datas).encode('utf-8')
    req = urllib2.Request(url, postdata, header)
    get_data = (urllib2.urlopen(req).read().decode('utf-8'))

    return get_data



#文字转换语音
def words_ro_audio(content,app_key,cust_account,org_tempKey,ext_terminalCode):

    url="http://dudu.yonyoutelecom.cn/VOICE/uploadVoiceNotice.do"
    timestamp=chartime()
    sign=design_SHA1(cust_account,org_tempKey,timestamp)
    #

    # 计费账号注册
    # url="http://dudu.yonyoutelecom.cn/orgacc/orgAccReg.do?app_key=%s&timestamp=%s&sign=%s&ext_orgCode=%s" \
    #     "&authData={'ext_orgName':'%s','ext_orgLinker':'%s','ext_orgEmail':'%s'}&ext_orgPhone=%s" % \
    #     (app_key,timestamp,sign,'qitongyun','企通云商','谷文峰','2881792624@qq.com','17602882849')
    #
    # print url
    # req = urllib2.Request(url)
    # get_data = (urllib2.urlopen(req).read())
    # print get_data


    datas={
        'app_key':app_key,
        'cust_account':cust_account,
        'timestamp':timestamp,
        'sign': sign,
        'ext_terminalCode': ext_terminalCode,
        'content': content,
    }

    """发送post请求"""
    get_data=send_post(url,datas)
    return get_data




#语音通知发送
def send_audio(app_key,cust_account,ext_terminalCode,mediaName,org_tempKey,caller,called,schedule_send_time,tts_content,push_url,batch_number):
    url='http://dudu.yonyoutelecom.cn/AUDEO/sendAudeoNoticeByMediaName.do'

    timestamp=chartime()
    sign=design_SHA1(cust_account,org_tempKey,timestamp)

    datas={
        'app_key':app_key,
        'cust_account':cust_account,
        'timestamp':timestamp,
        'sign': sign,
        'ext_terminalCode': ext_terminalCode,
        'caller': caller,
        'called':called,
        'mediaName':mediaName,
        'tts_content': tts_content,
        'push_url': push_url,
        'batch_number':batch_number
    }
    if schedule_send_time:
        datas.update({
            'schedule_send_time': schedule_send_time,
        })

    """发送post请求"""
    get_data=send_post(url,datas)
    return get_data




#语音调研
def voice_survey(app_key,cust_account,ext_terminalCode,mediaName,org_tempKey,caller,called,startDate,push_url,batch_number):
    url='http://dudu.yonyoutelecom.cn/IVRv4/IvrDial.do'

    timestamp=chartime()
    sign=design_SHA1(cust_account,org_tempKey,timestamp)

    datas={
        'app_key':app_key,
        'cust_account':cust_account,
        'timestamp':timestamp,
        'sign': sign,
        'ext_terminalCode': ext_terminalCode,
        'caller': caller,
        'called':called,
        # 'content':content,
        'mediaName': mediaName,
        'recvDigits': '1',
        # 'endDate': endDate,
        'push_url': push_url,
        'batch_number':batch_number
    }
    if startDate:
        datas.update({
            'startDate': startDate,
        })



    """发送post请求"""
    get_data=send_post(url,datas)
    return get_data


#取消语音通知或语音调研
def voice_canel( app_key, cust_account, ext_terminalCode, org_tempKey,batch_number):
    url = 'http://dudu.yonyoutelecom.cn/VOICE/cancelVoiceNotice.do'

    timestamp = chartime()
    sign = design_SHA1(cust_account, org_tempKey, timestamp)
    datas = {
        'app_key': app_key,
        'cust_account': cust_account,
        'timestamp': timestamp,
        'sign': sign,
        'ext_terminalCode': ext_terminalCode,
        'batch_number':batch_number
    }
    """发送post请求"""
    get_data=send_post(url,datas)
    return get_data




#.语音验证码
def voice_check( app_key, cust_account, ext_terminalCode, org_tempKey,called,content):
    url = 'http://dudu.yonyoutelecom.cn/VCAPTCHA/sendVoiceCaptcha.do'

    timestamp = chartime()
    sign = design_SHA1(cust_account, org_tempKey, timestamp)
    datas = {
        'app_key': app_key,
        'cust_account': cust_account,
        'timestamp': timestamp,
        'sign': sign,
        'ext_terminalCode': ext_terminalCode,
        'called': called,
        'content': content,
    }

    """发送post请求"""
    get_data=send_post(url,datas)
    return get_data




def search_message_resault(app_key,cust_account,org_tempKey,product_key):
    url = 'http://dudu.yonyoutelecom.cn/query/getresult.do'

    timestamp = chartime()
    sign = design_SHA1(cust_account, org_tempKey, timestamp)
    datas = {
        'app_key': app_key,
        'cust_account': cust_account,
        'timestamp': timestamp,
        'sign': sign,
        'product_key':product_key,
    }

    """发送post请求"""
    get_data = send_post(url,datas)
    return get_data

# send_message
#
# def voice_survey( app_key, cust_account, ext_terminalCode, mediaName, org_tempKey):
#     url = 'http://dudu.yonyoutelecom.cn/SMSv4/postSms.do'
#
#     timestamp = chartime()
#     sign = design_SHA1(cust_account, org_tempKey, timestamp)
#     datas = {
#         'app_key': app_key,
#         'cust_account': cust_account,
#         'timestamp': timestamp,
#         'sign': sign,
#         'ext_terminalCode': ext_terminalCode,
#         'called': called,
#         'msg_id': msg_id,
#         'template_code': template_code,
#         'template_params': template_params,
#     }
#
#     """发送post请求"""
#     get_data=send_post(url.datas)
#     return get_data


