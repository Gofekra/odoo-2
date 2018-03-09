# -*- coding: utf-8 -*-
import logging,json,urlparse
from odoo import http
from odoo.http import  request

_logger = logging.getLogger(__name__)
import  urllib2,urllib
from odoo.addons.ct_wechat.controllers.wx_api import  WeiXinLogin


class WeiXinData(http.Controller):

    # 微信公众号菜单调整接口---引导用户点击微信授权页面  ---        #POS菜单
    @http.route('/daili', type="http", auth='none', methods=['GET', 'POST'], csrf=False)
    def web_daili(self, **kwargs):
        home = WeiXinLogin()
        base_url = request.env['ir.config_parameter'].get_param('web.base.url')
        callbackurl = urlparse.urljoin(base_url, '/wx/login')
        url = {'redirect_uri': callbackurl}
        redirect_uri=urllib.urlencode(url)
        state='login'
        return  home.check_code(redirect_uri,state)

    # 微信公众号菜单调整接口---引导用户点击微信授权页面  ---        #零售流水
    @http.route('/sale_report', type="http", auth='none', methods=['GET', 'POST'], csrf=False)
    def web_sale_report(self, **kwargs):
        home = WeiXinLogin()
        base_url = request.env['ir.config_parameter'].get_param('web.base.url')
        callbackurl = urlparse.urljoin(base_url, '/wx/sale_report')
        url = {'redirect_uri': callbackurl}
        redirect_uri=urllib.urlencode(url)
        state = 'sale_report'
        return  home.check_code(redirect_uri,state)
