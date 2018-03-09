# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    after_done_state = [
        ('1', u'仅退货'),
        ('2', u'仅退款'),
        ('3', u'退货退款'),
    ]

    after_done_state = fields.Selection(after_done_state, string=u'售后状态', readonly=True)
