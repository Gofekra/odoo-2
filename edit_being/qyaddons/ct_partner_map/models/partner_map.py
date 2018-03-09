# -*- coding: utf-8 -*-

from odoo import SUPERUSER_ID, api
from odoo import models, fields, api,_
from odoo.tools.translate import _
import odoo.addons.decimal_precision as dp
import datetime
import time
import logging
from odoo.osv import osv, expression
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
_logger = logging.getLogger(__name__)


class res_partner(models.Model):
    _inherit = "res.partner"

    def _get_baidumap_address(self):
        res = dict.fromkeys(self.ids, dict())
        for i in self:
            state_name = i.state_id and i.state_id.name or ''
            name = i.name or ''
            city = i.city or ''
            street2 = i.street2 or ''
            street = i.street or ''
            address = ''.join([state_name, city, street2, street])
            if address == '':
                address = '上海市浦东新区浦东南路2250号创智B座4层'
            phone = i.phone or '400-820-8720'
            res[i.id] = "%s,%s,%s" % (address, name, phone)
        return res


    baidumap_address=fields.Char(string="Baidu Map Address",compute="_get_baidumap_address")

    def is_null(self, val):
        if(val):
            return val
        else:
            return " "

    @api.model
    def search_addres(self,id):
        if id:
            res=self.env['res.partner'].search([('id','=',int(id))])
            # country=res.country_id.name
            state=res.state_id.name
            city=res.city
            street=res.street
            street1 = res.street2
            mobile=""
            if res.mobile:
                mobile=res.mobile
            elif res.phone:
                mobile = res.phone

            add_name=res.name

            return {
                "name":add_name,
                "cite":self.is_null(state)+self.is_null(city)+self.is_null(street1)+self.is_null(street),
                "mobile":mobile
            }


    @api.model
    def search_key(self):
        key=self.env['ir.config_parameter'].search([('key','=','baidu_map_api_key')])
        if key:
            return key.value
        else:
            val={
                'key':"baidu_map_api_key",
                'value':"1Qi3ZNnerS3VbxvZvZkOfKOZ9i18W1Oy"
            }
            self.env['ir.config_parameter'].create(val)
            return val['value']






# class map_config_settings(models.TransientModel):
#     _inherit = 'base.config.settings'
#     # _name = 'map.config.settings'
#
#     # key = fields.Char(string="密钥", required=True, default_model='base.config.settings')
#     #
#     # def get_default_map(self,cr):
#     #     configs=self.env['base.config.settings'].search([])
#     #     length = len(configs)
#     #     if length != 0:
#     #         config = configs[-1]
#     #         return {"key": config.key}
#     #     else:
#     #         return {}



