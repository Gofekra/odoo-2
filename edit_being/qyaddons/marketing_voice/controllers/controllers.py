# -*- coding: utf-8 -*-
from odoo import http
from odoo import http
from odoo.http import request
import base64
import logging
import json
_logger = logging.getLogger(__name__)
import datetime

class CtDudu(http.Controller):


    @http.route('/send_voice/', type='http', auth="none", methods=['POST'], csrf=False)
    def voice_survey(self, **post):

        _logger.info('语音返回信息: json data %s', (post))  # debug
        date=post.get('date')
        call=date.get('callee')
        voice_line=request.env['dudu.voice.line'].search(['|',('phone','=',str(call)),('mobile','=',str(call))])
        if voice_line:
            voice_line.replied=datetime.datetime.now()
            voice_line.voice_check =True
            res={
                {"result": '0', "describe": "OK"}
            }
            return res
        else:
            return ""




    #7.5.6.语音调研用户按键结果推送【回调】
    @http.route('/voice_survey/', type='http', auth="none", methods=['GET', 'POST'], csrf=False)
    def voice_survey(self, **post):

        _logger.info('.语音调研返回信息: request.httprequest.data %s', (request.httprequest.data))  # debug
        params = json.loads(request.httprequest.data)
        date=params['data']
        for date_vals in date:
            session_id = str(date_vals['session_id'])
            callee = str(date_vals['callee'])
            digits=str(date_vals['digits'])
            voice_line = request.env['dudu.voice.line'].search(
                ['&', '|', ('phone', '=', callee), ('mobile', '=', callee),
                 ('session_id', '=', session_id)])
            if voice_line:
                voice_line.replied = datetime.datetime.now()
                voice_line.voice_check = True
                voice_line.digits=digits
                res={
                    {"result": '0', "describe": "OK"}
                }
                return res
            else:
                return ""

    #7.8.2.上行短信结果推送【回调】【POST】
    @http.route('/uplink_sms/', type='http', auth="none", methods=['POST'], csrf=False)
    def uplink_sms(self, **kw):
        res={
            {"result": '0', "describe": "OK"}
        }
        return res

