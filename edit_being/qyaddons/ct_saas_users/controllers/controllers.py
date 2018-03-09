# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
from odoo.addons.auth_signup.controllers.main import AuthSignupHome


class CtCenterManger(http.Controller):
    @http.route('/web/center_user', type='http', auth='public', website=True, csrf=False)
    def web_center_user(self, *args, **kw):
        user = kw['user']
        print user
        partner = user['partner_id']
        values = {
            'name': str(user['login']),
            'password': str(user['password_crypt']),
            'mobile': str(partner['mobile']),
            'email': str(partner['email']),
        }
        request.env['ct.center.res.users'].sudo().create(values)
        home = AuthSignupHome()
        home.web_auth_signup(confirm_password=u'congjainhua22', redirect=u'', tel=u'99999', name=u'oooo', token=u'',
                             login=u'oooo', password=u'congjianhua22')
