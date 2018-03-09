# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from werkzeug.exceptions import NotFound
from odoo import http
from odoo.http import request
import urllib
import urllib2
from odoo.addons.ct_dxb.controllers.main import WxinUser
import json

base_url = 'http://002.dxb.qitongyun.cn/'


class website_event(http.Controller):

    @http.route(['/weixin/', '/weixin/<path:in_type>', '/weixin/<path:in_type>/<int:id>'], type='http', auth="public",
                website=True)
    def events(self, in_type="home", id=None):
        obj = {}
        if id:  # 商品信息
            obj['wx_info'] = [0, 1, 2, 3]
        else:
            if in_type == "home":  # 首页
                url = base_url + "web/sale_summary"
                data = {}
                request_data = post_request(url, data)
                print request_data
            elif in_type == 'retail':
                url = base_url + "web/sale_report"
                data = {}
                request_data = post_request(url, data)
                obj[in_type] = {
                    'in_type': in_type,
                    'retail': request_data
                }
                print ('obj', obj)
                # weixin = WxinUser()
                #                 # weixin.sale_summary()
            else:  # 商品列表
                obj = {
                    'in_type': in_type,
                    'in_id': 1
                    # 'Dialog':{
                    #         'message':'你的信息输出有误 请重新输入！',
                    #         'title':'验证错误',
                    #         'show':True
                    #     }
                }
        return request.render('ct_dxb_weixin.%s' % in_type, obj)


def post_request(url, data):
    try:
        post_data = urllib.urlencode(data)
        request_data = urllib2.Request(url, post_data)
        response = urllib2.urlopen(request_data)
        request_data = response.read()
        return json.loads(request_data)
    except Exception as error:
        print error
        pass
