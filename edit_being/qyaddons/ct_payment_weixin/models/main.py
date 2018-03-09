# -*- coding: utf-8 -*-

try:
    import simplejson as json
except ImportError:
    import json
import logging
import pprint
import urllib2
import werkzeug

from lxml import etree

from odoo import http, SUPERUSER_ID
from odoo.osv import osv
from odoo.http import request
from . import util
import lxml
_logger = logging.getLogger(__name__)
import json

class WeixinController(http.Controller):
    _notify_url = '/payment/weixin/notify'
    def weixin_validate_data(self, post):
        json_data = {}
        if post:
            #方式一 解析返回信息
            for el in etree.fromstring(str(post)):
                json_data[el.tag] = el.text
        else:
            #方式二 主动查询结果
            json_data=request.env['payment.acquirer'].sudo().search_order()

        _logger.info("微信返回信息-----json：%s" % (json_data))
        #_KEY = request.registry['payment.acquirer']._get_weixin_key()
        _KEY ='be9aded460e78703b889f18e2915ea6c'
        _, prestr = util.params_filter(json_data)
        mysign = util.build_mysign(prestr, _KEY, 'MD5')
        if mysign != json_data.get('sign'):
            return 'false'

        _logger.info('weixin: validated data')
        return request.env['payment.transaction'].sudo().form_feedback(json_data, 'weixin')


    @http.route('/payment/weixin/notify', type='http', auth='public', methods = ['POST'],csrf=False)
    def weixin_notify(self,**post):
        _logger.info("微信返回信息： %s" % (post))
        if self.weixin_validate_data(post):
           return 'success'
        else:
           return ''


