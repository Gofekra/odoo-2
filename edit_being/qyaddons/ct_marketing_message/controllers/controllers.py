# -*- coding: utf-8 -*-
import babel.dates
import time, json
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

import werkzeug.urls
from werkzeug.exceptions import NotFound
import random
from odoo import http
from odoo import tools
from odoo.http import request
from odoo.tools.translate import _
from odoo.exceptions import UserError, ValidationError
import httplib
import urllib
import json


# 服务条款
class SmsEvent(http.Controller):
    def __init__(self):
        param = request.env()['ir.config_parameter']
        self.account = param.get_param('account') or ''
        self.password = param.get_param('password') or ''
        self.host_sign = param.get_param('host_sign') or ''
        self.host_marketing = param.get_param('host_marketing') or ''
        self.sms_heard = param.get_param('sms_heard') or ''
        # self.account = 'N6477034'
        # self.password = 'Hry7eSAjXa66bd'
        # self.host_sign = 'smssh1.253.com'
        # self.host_marketing = 'smsbj1.253.com'
        # self.sms_heard = '【253云通讯】'

    # 发送请求
    def send_post(self, datas, host, sms_send_uri):
        try:
            datas = json.dumps(datas)
            """发送post请求"""
            headers = {"Content-type": "application/json"}
            conn = httplib.HTTPConnection(host, port=80, timeout=30)
            conn.request("POST", sms_send_uri, datas, headers)
            response = conn.getresponse()
            response_str = response.read()
            conn.close()
            return response_str
        except Exception:
            return False

    # 发送短信验证码
    def commit_send_message(self, tel, code):
        sms_send_uri = "/msg/variable/json"
        phone = tel
        code = code
        params = phone + ',' + code
        msg = self.sms_heard + u"您好！验证码是：{$var}"
        print self.account
        print self.account
        datas = {
            'account': self.account,
            'password': self.password,
            'msg': msg,
            'params': params
        }

        send_result = self.send_post(datas, self.host_sign, sms_send_uri)
        print send_result
        if not send_result:
            return False
        else:
            sort_data = json.loads(send_result)
            print sort_data
            if int(sort_data["code"]) == 0:
                return code
            else:
                raise UserError(_(sort_data['errorMsg']))
