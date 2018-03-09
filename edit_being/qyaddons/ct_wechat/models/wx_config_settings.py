# -*- coding: utf-8 -*-
from openerp import models, fields, api

from ..rpc import oa_client


class wx_config_settings(models.TransientModel):
    _name = 'wx.config.settings'
    _description = u'对接公众号配置'
    # _order =
    _inherit = 'res.config.settings'

    wx_appid = fields.Char('AppId', )
    wx_AppSecret = fields.Char('AppSecret', )
    wx_AccessToken = fields.Char('当前AccessToken', readonly=True)
    wx_AESKey = fields.Char('EncodingAESKey', default='esGH2pMM98SwPMMQpXPG5Y5QawuL67E2aBvNP10V8Gl')
    wx_url = fields.Char('URL', readonly=True)
    wx_token = fields.Char('Token', default='token')


    def get_default_wx_AccessToken(self,fields):
        from odoo.http import request
        httprequest = request.httprequest
        return {
            'wx_AccessToken': '',
            'wx_url': 'http://%s/wx_handler' % httprequest.environ.get('HTTP_HOST', '').split(':')[0]
        }

    def get_default_wx_appid(self,fields):
        Param = self.env["ir.config_parameter"]
        return {
            'wx_appid': Param.get_param('wx_appid', default='appid'),
            'wx_AppSecret': Param.get_param( 'wx_AppSecret', default='appsecret'),
            'wx_token': Param.get_param('wx_token'),
            'wx_AESKey': Param.get_param('wx_AESKey'),
        }

    def set_wx_appid(self):
        Param = self.env["ir.config_parameter"]

        Param.set_param( 'wx_appid', self.wx_appid)
        Param.set_param( 'wx_AppSecret', self.wx_AppSecret)
        Param.set_param( 'wx_token', self.wx_token)
        Param.set_param('wx_AESKey', self.wx_AESKey)
