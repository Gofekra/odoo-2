# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError
import datetime
from dateutil.relativedelta import relativedelta
import pytz


@api.model
def _tz_get(self):
    # put POSIX 'Etc/*' entries at the end to avoid confusing users - see bug 1086728
    return [(tz, tz) for tz in sorted(pytz.all_timezones, key=lambda tz: tz if not tz.startswith('Etc/') else '_')]


class ResPartner(models.Model):
    _inherit = 'product.product'

    taxes_id = fields.Many2many("account.tax", string="销项税")
    supplier_taxes_id = fields.Many2many("account.tax", string="销项税")


class PosResUsers(models.Model):
    _inherit = 'res.partner'
    tz = fields.Selection(_tz_get, string='Language', default="Asia/Shanghai",
                          help="If the selected language is loaded in the system, all documents related to "
                               "this contact will be printed in this language. If not, it will be English.")


class DecimalPrecision(models.Model):
    _inherit = 'decimal.precision'

    @api.model
    def _edit_product_float(self):
        recode = self.search([('name', '=', 'Product Unit of Measure')])
        if recode:
            recode.digits = 2


class ChangeSales(models.TransientModel):
    _name = 'sales.change'
    _description = 'Change sales'

    name = fields.Char(string="订单")
    partner_id = fields.Many2one('res.partner', string="客户")
    product_return_moves = fields.One2many('sales.change.line', 'wizard_id', 'Moves')

    def action_change(self):
        # 先判断数量是否输入合理
        for lin in self.product_return_moves:
            if lin.quantity > lin.last_quantity:
                raise UserError(_("你所输入的退款数量大于剩余数量，请重新输入！"))

        pos_order = self.env['pos.order'].search([('name', '=', self.name)])
        old_product = []
        for lin in pos_order.lines:
            old_product.append(lin.product_id.id)

        new_product = []
        for lin in self.product_return_moves:
            new_product.append(lin.product_id.id)
        difference = list(set(old_product).difference(set(new_product)))
        lines = self.env['pos.order.line'].search([('order_id', '=', pos_order.id), ('product_id', 'in', new_product)])
        for lin_01 in lines:
            for lin_02 in self.product_return_moves:
                if lin_01.product_id.id == lin_02.product_id.id:
                    lin_01.refund_qty = lin_02.quantity + lin_01.refund_qty

        """Create a copy of order  for refund order"""
        PosOrder = self.env['pos.order']
        current_session = self.env['pos.session'].search([('state', '!=', 'closed'), ('user_id', '=', self.env.uid)],
                                                         limit=1)
        if not current_session:
            raise UserError(
                _('To return product(s), you need to open a session that will be used to register the refund.'))
        for order in pos_order:
            clone = order.copy({
                # ot used, name forced by create
                'name': order.name + _(' REFUND'),
                'session_id': current_session.id,
                'date_order': fields.Datetime.now(),
                'pos_reference': order.pos_reference,
                'slae_type': 'out',
            })
            PosOrder += clone

        for clone in PosOrder:
            for order_line in clone.lines:
                if order_line.product_id.id in difference:
                    order_line.unlink()
                else:
                    for order_line_01 in self.product_return_moves:
                        if order_line.product_id.id == order_line_01.product_id.id:
                            order_line.write({'qty': -order_line_01.quantity, 'refund_qty': 0.0})
        return {
            'name': _('Return Products'),
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'pos.order',
            'res_id': PosOrder.ids[0],
            'view_id': False,
            # 'context': self.env.context,
            'type': 'ir.actions.act_window',
            'target': 'current',
        }


class ChangeSalesLine(models.TransientModel):
    _name = "sales.change.line"
    _rec_name = 'product_id'

    product_id = fields.Many2one('product.product', string="产品", required=True)
    quantity = fields.Float("退货数量", required=True)
    last_quantity = fields.Float("剩余数量", required=True)
    wizard_id = fields.Many2one('sales.change', string="Wizard")

    @api.onchange('quantity')
    def _onchange_quantity(self):
        if self.quantity > self.last_quantity:
            self.quantity = self.last_quantity
            raise UserError(_("你所输入的退款数量大于剩余数量，请重新输入！"))
