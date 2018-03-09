# -*- coding: utf-8 -*-

import logging
from datetime import timedelta
from functools import partial

import psycopg2
import datetime
from odoo import api, fields, models, tools, _
from odoo.tools import float_is_zero
from odoo.exceptions import UserError
from odoo.http import request
import odoo.addons.decimal_precision as dp
_logger = logging.getLogger(__name__)

class pos_order(models.Model):
    _inherit = 'pos.order'

    merchantid=fields.Char(string="商户号")
    traceno = fields.Char(string="交易流水号")
    txntime = fields.Datetime(string="支付交易时间")
    indexcode = fields.Char(string="检索参考号")
    ext = fields.Selection([
        ('001', u'刷卡'),
        ('002', u'微信'),
        ('003', u'支付宝'),
    ], string="拓展信息")

    origin = fields.Many2one('pos.order',string="源单据")
    retufuse = fields.Boolean(string="退货")
    retufu_pay = fields.Boolean(string="退款")
    retufu_moneny=fields.Float(string="退款金额")


    @api.multi
    def refund(self):
        self.retufuse=True
        """Create a copy of order  for refund order"""
        PosOrder = self.env['pos.order']
        current_session = self.env['pos.session'].search([('state', '!=', 'closed'), ('user_id', '=', self.env.uid)],
                                                         limit=1)
        if not current_session:
            raise UserError(
                _('To return product(s), you need to open a session that will be used to register the refund.'))
        for order in self:
            clone = order.copy({
                # ot used, name forced by create
                'name': order.name + _(' REFUND'),
                'session_id': current_session.id,
                'date_order': fields.Datetime.now(),
                'pos_reference': order.pos_reference,
                'origin':self.id,
                'retufuse':False,
                'retufu_pay': False,
                'retufu_moneny': 0.0,
            })
            PosOrder += clone

        for clone in PosOrder:
            for order_line in clone.lines:
                order_line.write({'qty': -order_line.qty})
        return {
            'name': _('Return Products'),
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'pos.order',
            'res_id': PosOrder.ids[0],
            'view_id': False,
            'context': self.env.context,
            'type': 'ir.actions.act_window',
            'target': 'current',
        }
        #return  super(pos_order, self).refund()





    @api.multi
    def action_pos_order_paid(self):
        if not self.test_paid():
            raise UserError(_("Order is not paid."))



    #reset payment
    @api.model
    def action_pos_order_paid_reset(self,name):
        if not self.test_paid():
            raise UserError(_("Order is not paid."))
        res = self.env['pos.order'].search([('pos_reference', '=', name)])
        res.write({'state': 'paid'})
        return res.create_picking()


    #Cancel payment
    @api.model
    def action_unlink(self,name):
        res=self.env['pos.order'].search([('pos_reference','=',name)])
        resul=self.browse(res.id)
        resul.unlink()
        return name

    #Cancel payment
    @api.model
    def action_search_num(self,name):
        print name
        res=self.env['pos.order'].search([('pos_reference','=',name)])
        print res
        print res.name
        return res.name

