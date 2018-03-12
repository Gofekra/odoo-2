# -*- coding: utf-8 -*-
from odoo import models, fields, api

class Audiosettings(models.Model):
    _name = 'audio.config.settings'
    _description = u'配置'
    # _order =
    _inherit = 'res.config.settings'

    #音配参数
    APP_ID = fields.Char('APP_ID', )
    API_KEY = fields.Char('API_KEY', )
    SECRET_KEY = fields.Char('SECRET_KEY')

    #嘟嘟平台参数
    app_key = fields.Char('嘟嘟应用账号标识', )  #嘟嘟应用账号标识
    ext_orgCode = fields.Char('客户组织编码', ) #客户组织编码
    cust_account = fields.Char('计费账号标识') #计费账号标识
    org_tempKey=fields.Char('计费账号临时密钥')#计费账号临时密钥
    ext_terminalCode=fields.Char('使用通讯能力的用户ID') #使用通讯能力的用户ID

    def get_default_info(self,fields):
        Param = self.env["ir.config_parameter"]
        return {
            'APP_ID': Param.get_param('APP_ID', default='9877400'),
            'API_KEY': Param.get_param( 'API_KEY', default='gM44q5jAqqTNGiuz2G8GtRve'),
            'SECRET_KEY': Param.get_param('SECRET_KEY',default='PQjKUyF0LsDeTcRXcGzUIzbmLdsqCLM0'),

            'app_key': Param.get_param('app_key', default='420BAF8109315644921908D7D9EC6E45'),  #嘟嘟应用账号标识
            'ext_orgCode': Param.get_param('ext_orgCode', default='qitongyun'),  #客户组织编码
            'cust_account': Param.get_param('cust_account', default='qitongyun'), #计费账号标识
            'org_tempKey': Param.get_param('org_tempKey', default='EB96F4D47E3B1C5171A08B672566B29F'), #计费账号临时密钥
            'ext_terminalCode': Param.get_param('ext_terminalCode', default='qitongyun'),#使用通讯能力的用户ID
        }



    def set_info(self):
        Param = self.env["ir.config_parameter"]
        Param.set_param( 'APP_ID', self.APP_ID)
        Param.set_param( 'API_KEY', self.API_KEY)
        Param.set_param( 'SECRET_KEY', self.SECRET_KEY)

        Param.set_param( 'app_key', self.app_key)
        Param.set_param( 'ext_orgCode', self.ext_orgCode)
        Param.set_param( 'cust_account', self.cust_account)
        Param.set_param('org_tempKey', self.org_tempKey)
        Param.set_param('ext_terminalCode', self.ext_terminalCode)
