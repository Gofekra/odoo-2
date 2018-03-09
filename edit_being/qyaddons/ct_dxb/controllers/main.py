# -*- coding: utf-8 -*-
import babel.dates
import time, json
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

import werkzeug.urls
from werkzeug.exceptions import NotFound
import random
from odoo import http
from odoo import tools
from odoo.http import request
from odoo.tools.translate import _
from odoo.addons.web.controllers.main import ensure_db, Home
from odoo.exceptions import UserError, ValidationError

# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


"""
inherit:odoo
auther:cchong

"""
# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import json

from odoo import api, models
import logging, json
from odoo import http
from odoo.http import request
from odoo.addons import auth_signup

_logger = logging.getLogger(__name__)
import urllib2, urllib

import odoo


class Http(models.AbstractModel):
    _inherit = 'ir.http'

    @api.model
    def get_client(self):
        return request.env['ir.ui.menu'].load_menus(request.debug)


class DxbSignup(auth_signup.controllers.main.AuthSignupHome):
    def do_signup(self, qcontext):
        """ Shared helper that creates a res.partner out of a token """
        values = {key: qcontext.get(key) for key in ('login', 'name', 'password', 'tel')}
        assert values.values(), "The form was not properly filled in."
        assert values.get('password') == qcontext.get('confirm_password'), "Passwords do not match; please retype them."
        supported_langs = [lang['code'] for lang in request.env['res.lang'].sudo().search_read([], ['code'])]
        if request.lang in supported_langs:
            values['lang'] = request.lang
        self._signup_with_values(qcontext.get('token'), values)
        request.env.cr.commit()


class CorsUsers(http.Controller):
    @http.route('/cors/users', type="http", auth='none', methods=['GET', 'POST'], csrf=False)
    def cors_users(self, **kw):
        user = request.env['res.users'].sudo().search([('login', '=', kw['name'])], limit=1)
        if user:
            return user.sudo().password
        else:
            return 'faild'


class AuthSignupHome(Home):
    # 修改oauth密码
    @http.route('/web/commit_reset_token', type='http', auth='none', csrf=False)
    def commit_reset_token(self, *args, **kw):
        login = kw['login']
        user = request.env['res.users'].sudo().search([('login', '=', login)])
        if user:
            token = generate_verification_code2()
            print ('token:', token)
            user.write({'oauth_access_token': token})
            return {'oauth_access_token': token}
        else:
            return False


class WxinUser(http.Controller):
    # 零售流水路由
    @http.route('/web/sale_report', type="http", auth='none', methods=['GET', 'POST'], csrf=False)
    def sale_report(self, **kw):
        sale_report = request.env['pos.sale.report'].sudo().search([])
        data = []
        for item in sale_report:
            value = {
                'product_name': item.product_id.name or '',
                'qty': item.qty,
                'discount': item.discount,
                'price_unit': item.price_unit,
                'rece_unit': item.rece_unit,
                'amount_unit': item.amount_unit,
                'pos_categ_id': item.pos_categ_id.name or '',
                'partner_id': item.partner_id.name or '',
            }
            data.append(value)
        return json.dumps(data)

    # 零售汇总路由
    @http.route('/web/sale_summary', type="http", auth='none', methods=['GET', 'POST'], csrf=False)
    def sale_summary(self, **kw):
        request.env.cr.execute("""
                        SELECT Row_Number() over ( ) as id ,product_id ,qty ,amount_unit ,discount_unit,rece_unit 
                        FROM(
                          SELECT tb.product_id ,sum(tb.qty)as qty , sum(tb.qty*tb.price_unit) as amount_unit,
                          sum(CASE WHEN tb.discount=0 THEN 0 
                          ELSE qty*tb.price_unit*(1-(tb.discount)/100) END) as discount_unit,
                          sum( CASE WHEN tb.discount=0 THEN qty*tb.price_unit
                          ELSE qty*tb.price_unit*((tb.discount)/100) END )as rece_unit
                          FROM public.pos_order as ta 
                          left join pos_order_line as tb on ta.id=tb.order_id
                          left join product_product as tc on tb.product_id= tc.id
                          left join product_template as td on tc.product_tmpl_id=td.id
                          GROUP BY product_id 
                          )AS ta
                      """)
        sale_summary = request.env.cr.dictfetchall()
        return json.dumps(sale_summary)

    # 收款流水路由
    @http.route('/web/receivables_report', type="http", auth='none', methods=['GET', 'POST'], csrf=False)
    def receivables_report(self, **kw):
        sale_report = request.env['pos.receivables.report'].sudo().search([])
        data = []
        for item in sale_report:
            value = {
                'date_order': item.date_order,
                'name': item.name,
                'journal_id': item.journal_id.name or '',
                'pay_amount': item.pay_amount,
                'return_amount': item.return_amount,
                'profit_amount': item.profit_amount,
            }
            data.append(value)
        return json.dumps(data)

    # 收款汇总路由
    @http.route('/web/receivables_summary', type="http", auth='none', methods=['GET', 'POST'], csrf=False)
    def receivables_summary(self, **kw):
        request.env.cr.execute("""
              SELECT Row_Number() over ( ) as id , ty.*from (
               SELECT journal_id, sum(amount)as pay_amount,
                  NULL as return_amount, sum(amount)as profit_amount FROM(
                      SELECT  tc.journal_id,tc.amount FROM public.pos_order as ta 
                        left join pos_order_line as tb on ta.id=tb.order_id							             
                        left join account_bank_statement_line as tc on ta.id=tc.pos_statement_id 
                        WHERE ta.slae_type='in'  and (state='paid' or state='done')
                        GROUP BY ta.name,tc.journal_id,tc.amount,ta.date_order)
                      as aa GROUP BY journal_id
                  UNION ALL 
                SELECT journal_id, NULL AS pay_amount,
                    SUM(amount)AS return_amount, SUM(amount)AS profit_amount FROM(
                    SELECT tc.journal_id,tc.amount 
                        FROM PUBLIC.pos_order AS ta 
                        LEFT JOIN pos_order_line AS tb on ta.id=tb.order_id							              
                        LEFT JOIN  account_bank_statement_line AS tc ON ta.id=tc.pos_statement_id
                        WHERE ta.slae_type='out'  AND (state='paid' OR state='done')
                        GROUP BY tc.journal_id,tc.amount
                    )AS bb GROUP BY journal_id
                )as ty 
                            """)
        receivables_summary = request.env.cr.dictfetchall()
        return json.dumps(receivables_summary)

    # 收款汇总路由
    @http.route('/web/produce_rank', type="http", auth='none', methods=['GET', 'POST'], csrf=False)
    def produce_rank(self, **kw):
        request.env.cr.execute("""
              SELECT Row_Number() over ( ) as id ,product_id ,authentic_qty ,authentic_amount FROM(
              SELECT tb.product_id,sum(tb.qty)as authentic_qty, 
              sum(CASE WHEN tb.discount=0 THEN (tb.qty*tb.price_unit) 
              ELSE (tb.qty*tb.price_unit*((tb.discount)/100)) END) as authentic_amount
              FROM public.pos_order as ta 
              left join pos_order_line as tb on ta.id=tb.order_id
              WHERE ta.slae_type='in'  AND (state='paid' OR state='done')
              GROUP BY tb.product_id
              )AS ta
                            """)
        receivables_summary = request.env.cr.dictfetchall()
        return json.dumps(receivables_summary)


def generate_verification_code2():
    # 随机生成12位的随机字符
    code_list = []
    for i in range(4):
        random_num = random.randint(0, 9)
        a = random.randint(65, 90)
        b = random.randint(97, 122)
        random_uppercase_letter = chr(a)
        random_lowercase_letter = chr(b)
        code_list.append(str(random_num))
        code_list.append(random_uppercase_letter)
        code_list.append(random_lowercase_letter)
    verification_code = ''.join(code_list)
    return verification_code
