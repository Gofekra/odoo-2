# -*- coding: utf-8 -*-
import babel.dates
import time,json
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

import werkzeug.urls
from werkzeug.exceptions import NotFound
import random
from odoo import http
from odoo import tools
from odoo.http import request
from odoo.tools.translate import _
from odoo.addons.website.models.website import slug
from odoo.addons.web.controllers.main import ensure_db, Home
from odoo.exceptions import UserError, ValidationError

#服务条款
class website_event(http.Controller):
    @http.route(['/auth', '/auth/<path:page>'], type='http', auth="public", website=True)
    def events(self, page="sales"):
        
        page = 'ct_dxb_register.%s' % page
        return request.render(page)

class AuthSignupHome(Home):
    @http.route('/web/signup', type='http', auth='public', website=True)
    def web_auth_signup(self, *args, **kw):
        super(AuthSignupHome, self).web_auth_signup(*args, **kw)
        qcontext = self.get_auth_signup_qcontext()
        user=request.env["res.users"].sudo().search([("login", "=", qcontext.get("login"))])
        if user:
            user.partner_id.mobile=qcontext.get('tel')
            return super(AuthSignupHome, self).web_login(*args, **kw)

        return request.render('auth_signup.signup', qcontext)

    #发送短信验证码
    @http.route('/web/commit_send_message', type='json', auth='public', website=True)
    def commit_send_message(self,*args,**kw):
        name=kw['login']
        called =kw['tel']
        user = request.env['res.users'].sudo().search([('login','=',name)])
        if user and user.partner_id.mobile==called:
            code2 = generate_verification_code2()
            # 手机号码
            template_code = 'C91SSP'  # 模板编码
            template_params = [str(called), code2, "2"]  # 参数
            data = request.env['mark.message'].commit_send_message(called, template_code, template_params)
            sort_data = json.loads(data)
            print sort_data
            if sort_data['result'] == "0":
                return code2
                # return '2VI4Yx'
            else:
                raise UserError(_(sort_data['describe']))
        else:

            return ''



    #修改密码
    @http.route('/web/commit_reset_password', type='http', auth='public', website=True)
    def change_password_button(self,*args,**kw):
        name=kw['login']
        called =kw['tel']
        new_passwd=kw['password']
        user = request.env['res.users'].sudo().search([('login','=',name)])
        if user and user.partner_id.mobile==called:
            user.write({'password': new_passwd})
            return super(AuthSignupHome, self).web_login(*args, **kw)
        else:
            raise UserError(_("该用户不存在或者该手机号未绑定该账户"))


def generate_verification_code2():
    ''' 随机生成6位的验证码 '''
    code_list = []
    for i in range(2):
        random_num = random.randint(0, 9)  # 随机生成0-9的数字
        # 利用random.randint()函数生成一个随机整数a，使得65<=a<=90
        # 对应从“A”到“Z”的ASCII码
        a = random.randint(65, 90)
        b = random.randint(97, 122)
        random_uppercase_letter = chr(a)
        random_lowercase_letter = chr(b)
        code_list.append(str(random_num))
        code_list.append(random_uppercase_letter)
        code_list.append(random_lowercase_letter)
    verification_code = ''.join(code_list)

    return verification_code