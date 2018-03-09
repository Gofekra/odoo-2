# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request




class CtCrossRegistr(http.Controller):

    @http.route('/web/cross_registr/', type='http', auth='public', website=True)
    def cross_registr(self, **kw):
        valus={
            'user_database': kw['user_database'],
            'user_name': kw['user_name'],
            'user_password': kw['user_password'],
            'user_tel': kw['user_tel'],
        }
        res=request.env['public.user'].sudo().create_date(valus)
        if res:
            return valus
        else:
            return ''


    @http.route('/web/search_opeenid/', type='http', auth='public', website=True)
    def search_opeenid(self, **kw):
        valus={
            'user_database': kw['user_database'],
            'user_name': kw['user_name'],
            'user_password': kw['user_password'],
            'user_tel': kw['user_tel'],
            'openid': kw['openid']
        }
        res=request.env['public.user'].sudo().search_openid(valus)
        if res:
            return valus
        else:
            return ''