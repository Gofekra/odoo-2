# -*- coding: utf-'8' "-*-"
from main import WeixinController
import socket
try:
    import simplejson as json
except ImportError:
    import json
import logging
import urlparse
import urllib2
from lxml import etree
import random
import string,datetime,time
from odoo.tools.float_utils import float_compare
import util
from odoo.addons.payment.models.payment_acquirer import ValidationError
from odoo.http import request
from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class AcquirerWeixin(models.Model):
    _inherit = 'payment.acquirer'

    def _get_ipaddress(self):
        hostname = socket.gethostname()
        ip = '127.0.0.1'
        return ip

    provider = fields.Selection(selection_add=[('weixin', 'weixin')])
    weixin_appid = fields.Char(string='Weixin APPID', required_if_provider='weixin')
    weixin_mch_id = fields.Char(string=u'微信支付商户号', required_if_provider='weixin')
    weixin_key = fields.Char(string=u'API密钥 ', required_if_provider='weixin')
    weixin_secret = fields.Char(string='Weixin Appsecret', required_if_provider='weixin')

    def _get_weixin_urls(self, environment):
        if environment == 'prod':
            return {
                'weixin_url': 'https://api.mch.weixin.qq.com/pay/unifiedorder'
            }
        else:
            return {
                'weixin_url': 'https://api.mch.weixin.qq.com/pay/unifiedorder'
            }

    @api.one
    def _get_weixin_key(self):
        return self.weixin_key

    _defaults = {
        'fees_active': False,
    }

    def json2xml(self, json):
        string = ""
        for k, v in json.items():
            string = string + "<%s>" % (k) + str(v) + "</%s>" % (k)

        return string

    def _try_url(self, request, tries=3, context=None):
        done, res = False, None
        while (not done and tries):
            try:
                res = urllib2.urlopen(request)
                done = True
            except urllib2.HTTPError as e:
                res = e.read()
                e.close()
                if tries and res and json.loads(res)['name'] == 'INTERNAL_SERVICE_ERROR':
                    _logger.warning('Failed contacting Paypal, retrying (%s remaining)' % tries)
            tries = tries - 1
        if not res:
            pass
            # raise openerp.exceptions.
        result = res.read()
        res.close()
        return result

    def random_generator(self, size=6, chars=string.ascii_uppercase + string.digits):
        return ''.join([random.choice(chars) for n in xrange(size)])

    @api.multi
    def weixin_form_generate_values(self, tx_values):
        self.ensure_one()
        base_url = self.env['ir.config_parameter'].get_param('web.base.url')
        amount = int(tx_values.get('amount', 0) * 100)
        nonce_str =self.random_generator()
        data_post = {}
        now_time = time.strftime('%Y%m%d%H%M%S')
        data_post.update(
            {
                'appid': self.weixin_appid,
                'body': tx_values['reference'],
                'mch_id': self.weixin_mch_id,
                'nonce_str': nonce_str,
                'notify_url': '%s' % urlparse.urljoin(base_url, WeixinController._notify_url),
                'out_trade_no': now_time ,
                'spbill_create_ip': self._get_ipaddress(),
                'total_fee': amount,
                'trade_type': 'NATIVE',
            }
        )

        _, prestr = util.params_filter(data_post)
        sign = util.build_mysign(prestr, self.weixin_key, 'MD5')
        data_post['sign'] =sign
        # payid=self.env['payment.transaction'].search([('create_uid','=',self.env.uid),('state','=','draft'),('acquirer_id','=',self.id)])
        # for payid in payid:
        #     payid.acquirer_reference=data_post['out_trade_no']


        data_xml = "<xml>" + self.json2xml(data_post) + "</xml>"
        url = self._get_weixin_urls(self.environment)['weixin_url']
        request = urllib2.Request(url, data_xml)
        result = self._try_url(request, tries=3)
        data_post.update({
            'data_xml':data_xml,
        })
        return_xml = etree.fromstring(result)
        if return_xml.find('return_code').text == "SUCCESS" and return_xml.find('code_url').text != False:
            qrcode = return_xml.find('code_url').text
            data_post.update({
                'qrcode': qrcode,
            })
        else:
            return_code = return_xml.find('return_code').text
            return_msg = return_xml.find('return_msg').text
            raise ValidationError("%s, %s" % (return_code, return_msg))
        tx_values=data_post
        return  tx_values


    #点击付款之后 跳转的界面
    @api.multi
    def weixin_get_form_action_url(self):
        self.ensure_one()
        return self._get_weixin_urls(self.environment)['weixin_url']



    #主动查询支付交易订单情况
    def search_order(self):

        weixin_appid='wxb3be4c9e8f1add69'
        weixin_mch_id='1280015001'
        weixin_key='be9aded460e78703b889f18e2915ea6c'

        payid=self.env['payment.transaction'].search([('state','=','draft')])
        for payid in payid:
            out_trade_no= payid.acquirer_reference
        url = 'https://api.mch.weixin.qq.com/pay/orderquery'
        nonce_str =self.random_generator()
        data_post = {
            'appid':weixin_appid,
            'mch_id':weixin_mch_id,
            'out_trade_no': out_trade_no,
            'nonce_str': nonce_str,
        }

        _, prestr = util.params_filter(data_post)
        sign = util.build_mysign(prestr, weixin_key, 'MD5')
        data_post['sign'] = sign
        data_xml = "<xml>" + self.json2xml(data_post) + "</xml>"
        request = urllib2.Request(url, data_xml)
        result = self._try_url(request, tries=3)
        json = {}
        for el in etree.fromstring(str(result)):
            json[el.tag] = el.text

        return json


class TxWeixin(models.Model):
    _inherit = 'payment.transaction'

    weixin_txn_id = fields.Char(string='Transaction ID')
    weixin_txn_type = fields.Char(string='Transaction type')


    # --------------------------------------------------
    # FORM RELATED METHODS
    # --------------------------------------------------
    #付款交易订单查询是否存在
    def _weixin_form_get_tx_from_data(self, data):
        reference, txn_id = data.get('out_trade_no'), data.get('out_trade_no')
        if not reference or not txn_id:
            error_msg = 'weixin: received data with missing reference (%s) or txn_id (%s)' % (reference, txn_id)
            _logger.error(error_msg)
            raise ValidationError(error_msg)

        # find tx -> @TDENOTE use txn_id ?
        tx_ids = self.search([('acquirer_reference', '=', reference)])
        if not tx_ids or len(tx_ids) > 1:
            error_msg = 'weixin: received data for reference %s' % (reference)
            if not tx_ids:
                error_msg += '; no order found'
            else:
                error_msg += '; multiple order found'
            _logger.error(error_msg)
            raise ValidationError(error_msg)
        return tx_ids[0]

    #付款交易金额检查--交易币种检查
    def _weixin_form_get_invalid_parameters(self, data):
        invalid_parameters = []

        if float_compare(float(data.get('total_fee', '0.0')), self.amount, 2) != 0:
            invalid_parameters.append(('amount', data.get('total_fee'), '%.2f' % self.amount))
        if data.get('fee_type') != self.currency_id.name:
            invalid_parameters.append(('currency', data.get('fee_type'), self.currency_id.name))

        return invalid_parameters


    #交易验证完成之后 记录凭证信息
    def _weixin_form_validate(self, data):
        status = data.get('trade_state')
        data = {
            # 'acquirer_reference': data.get('out_trade_no'),
            'weixin_txn_id': data.get('out_trade_no'),
            'weixin_txn_type': data.get('fee_type'),
        }

        if status == 'SUCCESS':
            _logger.info('Validated weixin payment for tx %s: set as done' % (self.reference))
            data.update(state='done', date_validate=data.get('time_end', fields.datetime.now()))
            return self.write(data)

        else:
            error = 'Received unrecognized status for weixin payment %s: %s, set as error' % (self.reference, status)
            _logger.info(error)
            data.update(state='error', state_message=error)
            return self.write(data)
