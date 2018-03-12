# -*- coding: utf-8 -*-
from odoo import models, fields, api


class SmsConfig(models.Model):
    _name = 'sms.config.settings'
    _description = u'配置'
    _inherit = 'res.config.settings'
    # 短信参数
    _inherit = 'res.config.settings'
    # 253
    account = fields.Char('253账户')  # 253应用账号标识
    password = fields.Char('253密码')  # 253账号密码
    host_sign = fields.Char('验证模板请求地址')  # 253短信通知请求
    host_marketing = fields.Char('营销模板请求地址')  # 253营销请求
    sms_heard = fields.Char('头部签名模板')  # 253短信头部签名，例如：【253云通讯】

    def get_default_info(self, fields):
        Params = self.env["ir.config_parameter"]
        return {
            'account': Params.get_param('account', default='N6477034'),  # 253应用账号标识
            'password': Params.get_param('password', default='Hry7eSAjXa66bd'),  # 253账号密码
            'host_sign': Params.get_param('host_sign', default='smssh1.253.com'),  # 253短信通知模板地址
            'host_marketing': Params.get_param('host_marketing', default='smsbj1.253.com'),  # 253营销短信请求模板地址
            'sms_heard': Params.get_param('sms_heard', default='【253云通讯】'),  # 253签名模板
        }

    def set_info(self):
        Params = self.env["ir.config_parameter"]
        Params.set_param('account', self.account)
        Params.set_param('password', self.password)
        Params.set_param('host_sign', self.host_sign)
        Params.set_param('host_marketing', self.host_marketing)
        Params.set_param('sms_heard', self.sms_heard)