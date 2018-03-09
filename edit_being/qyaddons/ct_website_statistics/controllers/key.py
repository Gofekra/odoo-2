# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request

class Controller(http.Controller):

    @http.route('/search_key',type='http', auth="user", website=True)
    def key_authentication(self, **kwargs):
        key=request.env['ir.config_parameter'].search([('key','=','baidu_shangq_api_key')])
        if key:
            return key.value
        else:
            val={
                'key':"baidu_shangq_api_key",
                'value':"1263668332"
            }
            request.env['ir.config_parameter'].create(val)
            return val['value']
