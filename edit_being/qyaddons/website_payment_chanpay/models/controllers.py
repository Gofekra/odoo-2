# -*- coding: utf-8 -*-
from odoo import http
import json
import logging
import pprint
import urllib2
import werkzeug

from odoo import http
from odoo.http import request
from odoo import api, fields, models, _
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA
from base64 import b64decode
import func

_logger = logging.getLogger(__name__)
class CtChanpayWebsite(http.Controller):
    _return_url='/payment/chanpay/ipn'
    _notify_url = '/payment/chanpay/ipn/'
    https_verify_url = 'https://mapi.alipay.com/gateway.do?service=notify_verify&'
    http_verify_url = 'http://notify.alipay.com/trade/notify_query.do?'
    ALIPAY_PUBLIC_KEY_PATH = 'rsa_public_key.pem'

    def _get_return_url(self, **post):
        """ Extract the return URL from the data coming from alipay. """
        return_url = post.pop('return_url', '')
        if not return_url:
            custom = json.loads(post.pop('custom', False) or '{}')
            return_url = custom.get('return_url', '/')
        return return_url

    """
     * 获取返回时的签名验证结果
     * @param post 通知返回来的参数数组
     * @返回 签名验证结果
    """

    def getSignVeryfy(self, **post):
        key_sorted = sorted(post.keys())
        content = ''
        sign_type = post['sign_type']
        sign = post['sign']

        for key in key_sorted:
            if key not in ["sign", "sign_type"]:
                if post[key]:
                    content = content + key + "=" + post[key] + "&"
        content = content[:-1]
        content = content.encode("utf-8")
        isSign = False
        if sign_type.upper() == "RSA":
            public_key = request.env['payment.acquirer'].sudo().search([('name', '=', 'Chanpay')]).public_key
            isSign = func.rsaVerify(content, public_key, sign)
        return isSign

    """
     * 针对notify_url验证消息是否是支付宝发出的合法消息
     * @返回 验证结果
    """

    def verify_data(self, **post):
        if not post:
            return False
        else:
            isSign = self.getSignVeryfy(**post)
            if isSign:
                return True
            else:
                return False


    @http.route('/payment/chanpay/ipn', type='http', auth="none", methods=['POST'], csrf=False)
    def alipay_ipn(self, **post):
        """ Alipay IPN. """

        data = pprint.pformat(post)
        _logger.info('Beginning Alipay IPN form_feedback with post data %s', pprint.pformat(data))  # debug

        if self.verify_data(**post):
            txs = request.env['payment.transaction'].sudo().search([('reference', '=', post.get('outer_trade_no'))])
            res = {
                # 'chanpay_txn_type': data.get('inner_trade_no'),
                'acquirer_reference': post.get('outer_trade_no'),
                'partner_reference': post.get('buyer_id')
            }
            res.update(state='done', date_validate=data.get('gmt_payment', fields.datetime.now()))
            txs.write(res)

            order = request.env['sale.order'].sudo().search([('id', '=', txs.sale_order_id.id)])
            order.action_confirm()
            return 'success'
        else:
            txs = request.env['payment.transaction'].sudo().search([('reference', '=',  post.get('outer_trade_no'))])
            if txs:
                res = {
                    'state_message': post.get('inner_trade_no'),
                    'acquirer_reference': post.get('outer_trade_no'),
                }
                res.update(state='done', date_validate= fields.datetime.now())
                txs.write(res)
                order = request.env['sale.order'].sudo().search([('id', '=', txs.sale_order_id.id)])
                order.action_confirm()
                return 'success'



    @http.route('/payment/chanpay/refuse/', type='http', auth="none", methods=['POST'], csrf=False)
    def chanpay_refuse(self, **post):
        _logger.info('退款成功返回信息 ========= %s', pprint.pformat(post))  # debug
        if post:
            data=pprint.pformat(post)
            txs = request.env['payment.transaction'].sudo().search([('reference', '=', post.get('outer_trade_no'))])
            res = {
                'inner_trade_no': post.get('inner_trade_no'),
                'refund_status':'2',
                'gmt_refund': post.get('buyer_id'),
                'extension': post.get('extension'),
            }
            txs.write(res)
            return 'success'
        else:
            return 'fail'
