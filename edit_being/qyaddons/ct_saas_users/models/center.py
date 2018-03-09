# -*- coding: utf-8 -*-

from odoo import models, fields, api
import time


class ResPartner(models.Model):
    _inherit = 'res.partner'


    open_id = fields.Char(string='Openid')
    username = fields.Char(string='用户名')
    user_password = fields.Char(string='密码')
    about_user_ids = fields.One2many('res.partner.about.user', 'partner_id', string='关联用户', copy=False, readonly=True)
    _sql_constraints = [
        ('open_id_unique', 'unique (open_id)', 'openid不可重复')
    ]


class ResPartnerUser(models.Model):
    _name = 'res.partner.about.user'
    username = fields.Char(string='用户名')
    user_password = fields.Char(string='密码')
    open_id = fields.Char(string='Openid')
    mobile = fields.Char(string='手机号')
    partner_id = fields.Many2one('res.partner', string='Partner')
    _sql_constraints = [
        ('open_id_unique', 'unique (open_id)', 'openid不可重复')
    ]

