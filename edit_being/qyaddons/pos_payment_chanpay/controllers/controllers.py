# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
from . import util
import hashlib;
from Crypto.Cipher import DES3
import base64
import logging
import json
_logger = logging.getLogger(__name__)
import datetime


class CtChjiePos(http.Controller):

    global flag
    flag = 0

    @http.route('/payment/chgjiepos/NewSource', type='json', auth='public')
    def NewSource(self):
        global flag
        flag = 0

    @http.route('/payment/chgjiepos/EventSource', type='json', auth='public')
    def EventSource(self):
        global flag
        return flag


    #http://gwf.qitong.work/payment/chgjiepos/notify 支付结果返回地址
    @http.route('/payment/chgjiepos/notify', type='http', auth='public', methods = ['POST'],csrf=False)
    def weixin_notify(self,**post):
        def create_key(sk):
            r = hashlib.md5(sk).digest()
            return r + r[:8]

        def init_str(s):
            l = len(s) % 16
            if l != 0:
                c = 16 - l
                s += chr(c) * c
            return s

        _logger.info('畅捷支付返回信息: json data %s', (post))  # debug
        for data in post:
            post = json.loads(data)
            tranCode=post['tranCode']#交易码

            if tranCode=='0101': #订单查询请求(QueryOrderDetail) :
                orderId=post['orderId']#订单编号
                merchantId=post['merchantId']#商户号
                money=request.env['pos.order'].sudo().search([('name','=',orderId)]).amount_total #支付金额
                key="137560935D96F78DF77B32776E66ED7E"
                data_post={
                    'tranCode':'0102',
                    'orderId': orderId,
                    'merchantId': merchantId,
                    'money': money*10,
                }
                _, prestr = util.params_filter(data_post)
                keys =create_key(key)
                ss = init_str(prestr)
                des3 = DES3.new(keys, DES3.MODE_ECB)
                res2 = des3.encrypt(ss)
                sign = base64.standard_b64encode(res2)
                data_post.update({
                    'sign': sign,
                })
                b = json.dumps(data_post)
                return b

            if tranCode == '0103':  # 订单消费(OrderConsumeResponse) :
                orderId = post['orderId']  # 订单编号
                tranTime = post['tranTime']  # 交易时间
                traceNo = post['traceNo']  # 交易流水号
                merchantId = post['merchantId']  # 商户号
                money = post['money']  # 支付金额
                txnCode = post['txnCode']  # 响应结果
                txnTime = post['txnTime']  # 支付交易时间
               # traceauditno = post['traceauditno']  # 流水号
                indexCode = post['indexCode']  # 检索参考号
                ext = post['ext']  # 拓展信息{001 刷卡、002 微信、003 支付宝}
                if txnCode=='00':#支付成功
                    order = request.env['pos.order'].sudo().search([('name', '=', orderId)])  # 支付金额
                    order.write({'traceno': traceNo})
                    order.write({'merchantid': merchantId})
                    order.write({'txntime':datetime.datetime.now()})
                    order.write({'indexcode': indexCode})
                    order.write({'ext': ext})
                    key= "137560935D96F78DF77B32776E66ED7E"
                    data_post = {
                        'tranCode': '0104',
                        'tranTime': tranTime,
                        'traceNo': traceNo,
                        'txnCode':txnCode,
                    }
                    _, prestr = util.params_filter(data_post)
                    keys = create_key(key)
                    ss = init_str(prestr)
                    des3 = DES3.new(keys, DES3.MODE_ECB)
                    res2 = des3.encrypt(ss)
                    sign = base64.standard_b64encode(res2)
                    data_post.update({
                        'sign': sign,
                    })
                    b = json.dumps(data_post)
                    global flag
                    flag=1

                    return b

            if tranCode == '0103' and post['orgIndexCode']:  # 订单撤销() :
                orderId = post['orderId']  # 订单编号
                tranTime = post['tranTime']  # 交易时间
                traceNo = post['traceNo']  # 交易流水号
                merchantId = post['merchantId']  # 商户号
                money = post['money']  # 支付金额
                txnCode = post['txnCode']  # 响应结果
                txnTime = post['txnTime']  # 支付交易时间
                # traceauditno = post['traceauditno']  # 流水号
                indexCode = post['indexCode']  # 检索参考号
                ext = post['ext']  # 拓展信息{001 刷卡、002 微信、003 支付宝}

                if txnCode == '00':  # 支付成功
                    order = request.env['pos.order'].sudo().search([('name', '=', orderId)])
                    order.write({'retufu_pay': True})
                    order.write({'retufu_moneny': post['money']})
                    key = "137560935D96F78DF77B32776E66ED7E"
                    data_post = {
                        'tranCode': '0104',
                        'tranTime': tranTime,
                        'traceNo': traceNo,
                        'txnCode': txnCode,
                    }
                    _, prestr = util.params_filter(data_post)
                    keys = create_key(key)
                    ss = init_str(prestr)
                    des3 = DES3.new(keys, DES3.MODE_ECB)
                    res2 = des3.encrypt(ss)
                    sign = base64.standard_b64encode(res2)
                    data_post.update({
                        'sign': sign,
                    })
                    b = json.dumps(data_post)
                    return b
