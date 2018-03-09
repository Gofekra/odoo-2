# -*- coding: utf-8 -*-
from odoo import api, models, fields, SUPERUSER_ID, _
from odoo.exceptions import UserError, ValidationError
from odoo.osv import osv
import xmlrpclib
import types

class Orderline(models.Model):
    _inherit = 'sale.order.line'


    @api.model
    def search_stock(self,id):
        print id

        res=self.env['sale.order.line'].search([('id','=',id)])
        qty_available=res.product_id.qty_available#现存量
        virtual_available=res.product_id.virtual_available

        price_com=self.env['product.price'].search([('pruduct_id','=',res.product_id.product_tmpl_id.id)],limit=1)

        data = [
            {'name':'现存量','val':qty_available},
            {'name': '可用量', 'val': virtual_available},
            {'name': '销售助理', 'val': str(price_com.assistant_price_start)+'-'+str(price_com.assistant_price_end)},
            {'name': '销售工程师', 'val': str(price_com.engineer_price_start) + '-' + str(price_com.engineer_price_end)},
            {'name': '销售经理', 'val': str(price_com.smanager_price_start) + '-' + str(price_com.smanager_price_end)},
            {'name': '产品经理', 'val': str(price_com.pmanager_price_start) + '-' + str(price_com.panager_price_end)},
            {'name': '总经理', 'val': str(price_com.gmanager_price_start) + '-' + str(price_com.gmanager_price_end)}
        ]

        return data


class PurchaseOrderline(models.Model):
    _inherit = 'purchase.order.line'


    @api.model
    def search_stock(self,id):
        print id

        res=self.env['purchase.order.line'].search([('id','=',id)])
        qty_available=res.product_id.qty_available#现存量
        virtual_available=res.product_id.virtual_available
        # outgoing_qty = res.product_id.outgoing_qty*-1
        # incoming_qty = res.product_id.incoming_qty
        return {
            '现存量':qty_available,
            '可用量':virtual_available
            }
