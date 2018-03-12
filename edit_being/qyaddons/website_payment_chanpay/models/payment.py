# coding: utf-8

import json
import logging
import urlparse
import func
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
import string, datetime, time
from odoo.osv import osv
from odoo import api, fields, models, _
from odoo.addons.payment.models.payment_acquirer import ValidationError
from odoo.tools.float_utils import float_compare
import datetime

_logger = logging.getLogger(__name__)


class Acquirerchanpay(models.Model):
    _inherit = 'payment.acquirer'

    provider = fields.Selection(selection_add=[('chanpay', 'Chanpay')])
    service = fields.Char('接口名称', required_if_provider="chanpay", groups='base.group_user')
    partner_id = fields.Char('合作者身份ID', groups='base.group_user')
    private_key = fields.Text(string="私钥", groups='base.group_user')
    public_key = fields.Text(string="公钥", groups='base.group_user')
    form_url = fields.Char(string="请求地址")

    @api.model
    def _get_chanpay_urls(self, environment):
        """ chanpay URLS """
        if environment == 'prod':
            return {
                'form_url': self.form_url,
            }
        else:
            return {
                'form_url': self.form_url,
            }

    @api.multi
    def chanpay_compute_fees(self, amount, currency_id, country_id):
        _return_url = '/payment/chanpay/ipn/'
        if not self.fees_active:
            return 0.0
        country = self.env['res.country'].browse(country_id)
        if country and self.company_id.country_id.id == country.id:
            percentage = self.fees_dom_var
            fixed = self.fees_dom_fixed
        else:
            percentage = self.fees_int_var
            fixed = self.fees_int_fixed
        fees = (percentage / 1.0 * amount + fixed) / (1 - percentage / 1.0)
        return fees

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

    @api.multi
    def chanpay_form_generate_values(self, values):
        print values
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        _return_url = 'chanpay/_return_url'
        chanpay_tx_values = dict(values)
        order= self.env['sale.order'].sudo().search([('name','=',values['reference'])])
        name = ""
        if order:
            for line in order.order_line:
                name+=line.product_id.name+";"
        else:
            name = "Pay Product"
        chanpay_tx_values = ({
            # basic parameters
            'is_anonymous': 'Y',
            '_input_charset': 'UTF-8',
            'is_returnpayurl': 'N',
            'notify_url': '%s' % urlparse.urljoin(base_url, '/payment/chanpay/ipn/'),
            'out_trade_no': values['reference'],
            'partner_id': self.partner_id,
            'product_name':name,
            'return_url': '%s' % urlparse.urljoin(base_url, '/shop/payment/validate'),
            'service': self.service,
            'sign_type': 'RSA',
            'trade_amount': float(values['amount']),
            'version': '1.0',
        })

        sign_values = {
            'is_anonymous': 'Y',
            '_input_charset': 'UTF-8',
            'is_returnpayurl': 'N',
            'notify_url': '%s' % urlparse.urljoin(base_url, '/payment/chanpay/ipn/'),
            'out_trade_no': values['reference'],
            'partner_id': self.partner_id,
            'product_name': name,
            'return_url': '%s' % urlparse.urljoin(base_url, '/shop/payment/validate'),
            'service': self.service,
            'trade_amount': float(values['amount']),
            'version': '1.0',
        }
        params, sign = func.buildRequestMysign(sign_values, self.private_key)
        chanpay_tx_values.update({
            'sign': sign,
        })
        # url = self._get_chanpay_urls(self.environment)['form_url']
        #
        # _, prestr = func.params_filter_add(chanpay_tx_values)
        # geturl=url+prestr
        # request = urllib2.Request(geturl)
        # get_data = urllib2.urlopen(request).read()
        #
        # print get_data
        return chanpay_tx_values

    @api.multi
    def chanpay_get_form_action_url(self):
        return self._get_chanpay_urls(self.environment)['form_url']


class Txchanpay(models.Model):
    _inherit = 'payment.transaction'

    # chanpay_txn_type = fields.Char('Transaction type')
    inner_trade_no = fields.Char(string="退款交易订单号")
    refund_status = fields.Selection( [('1',u'退款中'),('2',u'退款完成')], u'退款状态', )
    gmt_refund = fields.Date(string="交易退款时间")
    extension = fields.Char(string="备注")

    def refuse_money(self):
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        url = self.acquirer_id.form_url
        valus = {
            '_input_charset': 'UTF-8',
            'notify_url': '%s' % urlparse.urljoin(base_url, '/payment/chanpay/refuse/'),
            'orig_outer_trade_no': self.acquirer_reference,
            'outer_trade_no': self.reference,
            'partner_id': self.acquirer_id.partner_id,
            'refund_amount': self.amount,
            'service': 'cjt_create_refund',
            'sign_type': 'RSA',
            'version': '1.0',
        }
        params, sign = func.buildRequestMysign(valus, self.acquirer_id.private_key)
        valus.update({
            'sign': sign,
        })
        _, prestr = func.params_filter_add(valus)
        geturl = url + prestr
        #raise osv.except_osv(u'警告', geturl)
        request = urllib2.Request(geturl)
        data = urllib2.urlopen(request).read()
        get_data = json.loads(data)
        if get_data:
            if 'error_message' in get_data:
                raise osv.except_osv(u'警告', get_data.get('error_message')+"===="+get_data.get('memo'))
            else:
               self.refund_status='1'
    # --------------------------------------------------
    # FORM RELATED METHODS
    # --------------------------------------------------

    @api.model
    def _chanpay_form_get_tx_from_data(self, data):
        reference = data.get('outer_trade_no')

        # find tx -> @TDENOTE use txn_id ?
        txs = self.env['payment.transaction'].search([('reference', '=', reference)])
        if not txs or len(txs) > 1:
            error_msg = 'chanpay: received data for reference %s' % (reference)
            if not txs:
                error_msg += '; no order found'
            else:
                error_msg += '; multiple order found'
            _logger.info(error_msg)
            raise ValidationError(error_msg)
        return txs[0]

    @api.multi
    def _chanpay_form_get_invalid_parameters(self, data):
        invalid_parameters = []
        return invalid_parameters

    @api.multi
    def _chanpay_form_validate(self, data):
        status = data.get('trade_status')
        res = {
            'chanpay_txn_type': data.get('inner_trade_no'),
            'acquirer_reference': data.get('outer_trade_no'),
            'partner_reference': data.get('buyer_id')
        }
        if status in ['TRADE_FINISHED', 'TRADE_SUCCESS']:
            _logger.info('Validated chanpay payment for tx %s: set as done' % (self.reference))
            res.update(state='done', date_validate=data.get('gmt_payment', fields.datetime.now()))
            return self.write(res)
        else:
            error = 'Received unrecognized status for chanpay payment %s: %s, set as error' % (self.reference, status)
            _logger.info(error)
            res.update(state='error', state_message=error)
            return self.write(res)