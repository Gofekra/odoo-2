# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError
import datetime
from dateutil.relativedelta import relativedelta
import odoo.addons.decimal_precision as dp


class PosOrder(models.Model):
    _inherit = 'pos.order'

    slae_type = fields.Selection([
        ('in', '零售'),
        ('out', '退货')
    ], string="销售类型", default='in')

    @api.model
    def _amount_line_tax(self, line, fiscal_position_id):
        taxes = line.tax_ids.filtered(lambda t: t.company_id.id == line.order_id.company_id.id)
        if fiscal_position_id:
            taxes = fiscal_position_id.map_tax(taxes, line.product_id, line.order_id.partner_id)
        if line.discount == 0:
            price = line.price_unit
        else:
            price = line.price_unit * (line.discount / 100.0)
        taxes = taxes.compute_all(price, line.order_id.pricelist_id.currency_id, line.qty, product=line.product_id,
                                  partner=line.order_id.partner_id or False)['taxes']
        return sum(tax.get('amount', 0.0) for tax in taxes)

    def _create_account_move_line(self, session=None, move=None):
        # Tricky, via the workflow, we only have one id in the ids variable
        """Create a account move line of order grouped by products or not."""
        IrProperty = self.env['ir.property']
        ResPartner = self.env['res.partner']

        if session and not all(session.id == order.session_id.id for order in self):
            raise UserError(_('Selected orders do not have the same session!'))

        grouped_data = {}
        have_to_group_by = session and session.config_id.group_by or False
        rounding_method = session and session.config_id.company_id.tax_calculation_rounding_method

        for order in self.filtered(lambda o: not o.account_move or o.state == 'paid'):
            current_company = order.sale_journal.company_id
            account_def = IrProperty.get(
                'property_account_receivable_id', 'res.partner')
            order_account = order.partner_id.property_account_receivable_id.id or account_def and account_def.id
            partner_id = ResPartner._find_accounting_partner(order.partner_id).id or False
            if move is None:
                # Create an entry for the sale
                journal_id = self.env['ir.config_parameter'].sudo().get_param(
                    'pos.closing.journal_id_%s' % current_company.id, default=order.sale_journal.id)
                move = self._create_account_move(
                    order.session_id.start_at, order.name, int(journal_id), order.company_id.id)

            def insert_data(data_type, values):
                # if have_to_group_by:
                values.update({
                    'partner_id': partner_id,
                    'move_id': move.id,
                })

                if data_type == 'product':
                    key = ('product', values['partner_id'],
                           (values['product_id'], tuple(values['tax_ids'][0][2]), values['name']),
                           values['analytic_account_id'], values['debit'] > 0)
                elif data_type == 'tax':
                    key = ('tax', values['partner_id'], values['tax_line_id'], values['debit'] > 0)
                elif data_type == 'counter_part':
                    key = ('counter_part', values['partner_id'], values['account_id'], values['debit'] > 0)
                else:
                    return

                grouped_data.setdefault(key, [])

                if have_to_group_by:
                    if not grouped_data[key]:
                        grouped_data[key].append(values)
                    else:
                        current_value = grouped_data[key][0]
                        current_value['quantity'] = current_value.get('quantity', 0.0) + values.get('quantity', 0.0)
                        current_value['credit'] = current_value.get('credit', 0.0) + values.get('credit', 0.0)
                        current_value['debit'] = current_value.get('debit', 0.0) + values.get('debit', 0.0)
                else:
                    grouped_data[key].append(values)

            # because of the weird way the pos order is written, we need to make sure there is at least one line,
            # because just after the 'for' loop there are references to 'line' and 'income_account' variables (that
            # are set inside the for loop)
            # TOFIX: a deep refactoring of this method (and class!) is needed
            # in order to get rid of this stupid hack
            assert order.lines, _('The POS order must have lines when calling this method')
            # Create an move for each order line
            cur = order.pricelist_id.currency_id
            for line in order.lines:
                amount = line.price_subtotal

                # Search for the income account
                if line.product_id.property_account_income_id.id:
                    income_account = line.product_id.property_account_income_id.id
                elif line.product_id.categ_id.property_account_income_categ_id.id:
                    income_account = line.product_id.categ_id.property_account_income_categ_id.id
                else:
                    raise UserError(_('Please define income '
                                      'account for this product: "%s" (id:%d).')
                                    % (line.product_id.name, line.product_id.id))

                name = line.product_id.name
                if line.notice:
                    # add discount reason in move
                    name = name + ' (' + line.notice + ')'

                # Create a move for the line for the order line
                insert_data('product', {
                    'name': name,
                    'quantity': line.qty,
                    'product_id': line.product_id.id,
                    'account_id': income_account,
                    'analytic_account_id': self._prepare_analytic_account(line),
                    'credit': ((amount > 0) and amount) or 0.0,
                    'debit': ((amount < 0) and -amount) or 0.0,
                    'tax_ids': [(6, 0, line.tax_ids_after_fiscal_position.ids)],
                    'partner_id': partner_id
                })

                # Create the tax lines
                taxes = line.tax_ids_after_fiscal_position.filtered(lambda t: t.company_id.id == current_company.id)
                if not taxes:
                    continue
                # price = line.price_unit * ((line.discount or 0.0) / 100.0)
                if line.discount == 0:
                    price = line.price_unit
                else:
                    price = line.price_unit * (line.discount / 100.0)
                for tax in taxes.compute_all(price, cur, line.qty)['taxes']:
                    insert_data('tax', {
                        'name': _('Tax') + ' ' + tax['name'],
                        'product_id': line.product_id.id,
                        'quantity': line.qty,
                        'account_id': tax['account_id'] or income_account,
                        'credit': ((tax['amount'] > 0) and tax['amount']) or 0.0,
                        'debit': ((tax['amount'] < 0) and -tax['amount']) or 0.0,
                        'tax_line_id': tax['id'],
                        'partner_id': partner_id
                    })

            # round tax lines per order
            if rounding_method == 'round_globally':
                for group_key, group_value in grouped_data.iteritems():
                    if group_key[0] == 'tax':
                        for line in group_value:
                            line['credit'] = cur.round(line['credit'])
                            line['debit'] = cur.round(line['debit'])

            # counterpart
            insert_data('counter_part', {
                'name': _("Trade Receivables"),  # order.name,
                'account_id': order_account,
                'credit': ((order.amount_total < 0) and -order.amount_total) or 0.0,
                'debit': ((order.amount_total > 0) and order.amount_total) or 0.0,
                'partner_id': partner_id
            })

            order.write({'state': 'done', 'account_move': move.id})

        all_lines = []
        for group_key, group_data in grouped_data.iteritems():
            for value in group_data:
                all_lines.append((0, 0, value), )
        if move:  # In case no order was changed
            move.sudo().write({'line_ids': all_lines})
            move.sudo().post()
        return True

    @api.model
    def create_from_ui(self, orders):
        orders_data = []
        for data in orders:
            lines = data['data']['lines']
            orders_lines = []
            for line in lines:
                product_id = line[2].get('product_id')
                uom_id = self.env['product.product'].browse(product_id).product_tmpl_id.uom_id
                line[2]['product_uom'] = uom_id.id
                orders_lines.append(line)
                data['data']['lines'] = orders_lines
            orders_data.append(data)
        return super(PosOrder, self).create_from_ui(orders_data)

    @api.multi
    def refund(self):
        count = self.env['pos.order.line'].search_count([('order_id', '=', self.id)])
        lins_count = 0.0
        for lin_count in self.lines:
            if lin_count.qty == lin_count.refund_qty:
                lins_count += 1
        if count == lins_count:
            raise UserError(
                _('该订单中的商品已全部退货，无法继续执行退货！'))

        ctx = {
            'default_name': self.name,
            'default_partner_id': self.partner_id.id,
            'default_product_return_moves': [],
        }

        for lin in self.lines:
            line_vals = {}
            if lin_count.qty != lin_count.refund_qty:
                line_vals.update(
                    {
                        'product_id': lin.product_id.id,
                        'quantity': lin.qty - lin.refund_qty,
                        'last_quantity': lin.qty - lin.refund_qty,
                    })
                ctx['default_product_return_moves'].append((0, 0, line_vals))

        return {
            'name': '退货操作',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'sales.change',
            'view_id': self.env.ref('ct_dxb.sales_change_form').id,
            'type': 'ir.actions.act_window',
            'context': ctx,
            'target': 'new',
        }

    def unlink(self):
        for self in self:
            if self.slae_type == 'out' and self.state == 'draft':
                # 如果删除未确认的退货订单，则还原退回数量
                data = self.search([('pos_reference', '=', self.pos_reference), ('slae_type', '=', 'in')])
                for lines_in in data.lines:
                    for lines_out in self.lines:
                        if lines_in.product_id.id == lines_out.product_id.id:
                            lines_in.refund_qty = lines_in.refund_qty + lines_out.qty

            return super(PosOrder, self).unlink()

    def get_datetime(self, day):
        # 根据数据获取开始日期以及结束日期
        if day == 1:
            # 获取今天的日期
            start_time = datetime.datetime.now().strftime('%Y-%m-%d 00:00:00')
            end_time = datetime.datetime.now().strftime('%Y-%m-%d 23:59:59')
        if day == 2:
            start_time = (datetime.date.today() + relativedelta(days=-1)).strftime('%Y-%m-%d 00:00:00')
            end_time = (datetime.date.today() + relativedelta(days=-1)).strftime('%Y-%m-%d 23:59:59')
        if day == 3:
            start_time = (datetime.date.today() + datetime.timedelta(-(datetime.date.today().weekday()))).strftime(
                '%Y-%m-%d 00:00:00')
            end_time = datetime.datetime.now().strftime('%Y-%m-%d 23:59:59')
        if day == 4:
            start_time = (datetime.date.today() + relativedelta(months=-1)).strftime('%Y-%m-01 00:00:00')
            end_time = datetime.datetime.now().strftime('%Y-%m-%d 23:59:59')

        return start_time, end_time

    @api.model
    def search_pos_result(self, start_time, end_time):
        if start_time in [1, 2, 3, 4]:
            start_time, end_time = self.get_datetime(start_time)
        data = {}
        # 销售额
        sql_01 = """
           select sum((case  when discount>0  then qty*price_unit*(discount/100) else qty*price_unit end))
            FROM public.pos_order as ta 
            left join pos_order_line as tb on ta.id=tb.order_id
            where ta.date_order>='%s' and  ta.date_order<='%s'
            and ta.slae_type='in' and (ta.state='paid' or ta.state='done')
        """ % (start_time, end_time)
        self.env.cr.execute(sql_01)
        data.update({
            'sale_amount': self.env.cr.dictfetchall()[0]['sum']
        })

        # 销售笔数

        sql_02 = """
           SELECT count(*) FROM public.pos_order as ta 
            where ta.date_order>='%s' and  ta.date_order<='%s'
            and ta.slae_type='in' and (ta.state='paid' or ta.state='done')
          """ % (start_time, end_time)

        self.env.cr.execute(sql_02)
        data.update({
            'sale_count': self.env.cr.dictfetchall()[0]['count']
        })

        # 退款额
        sql_03 = """
        select sum((case  when discount>0  then qty*price_unit*(discount/100) else qty*price_unit end))
          FROM public.pos_order as ta 
        left join pos_order_line as tb on ta.id=tb.order_id
        where ta.date_order>='%s' and  ta.date_order<='%s'
        and ta.slae_type='out' and (ta.state='paid' or ta.state='done')
        """ % (start_time, end_time)

        self.env.cr.execute(sql_03)
        data.update({
            'refund_amount': self.env.cr.dictfetchall()[0]['sum']
        })

        # 退款笔数

        sql_04 = """
              SELECT count(*)
              FROM public.pos_order as ta 
             where ta.date_order>='%s' and  ta.date_order<='%s'
            and ta.slae_type='out' and (ta.state='paid' or ta.state='done')
        """ % (start_time, end_time)

        self.env.cr.execute(sql_04)
        data.update({
            'refund_count': self.env.cr.dictfetchall()[0]['count']
        })

        # 根据付款方式统计收款情况

        sql_05 = """
	 
        select tb.name ,sum(amount) as amount from pos_order as po 
        left join account_bank_statement_line as ta  on ta.pos_statement_id=po.id
        left join account_journal as tb on ta.journal_id=tb.id
            where  po.date_order>='%s' and  po.date_order<='%s'
        group by tb.name
        """ % (start_time, end_time)

        self.env.cr.execute(sql_05)
        re = []
        pay = self.env.cr.dictfetchall()
        for result in pay:
            if result['name']:
                re.append(
                    {
                        'name': result['name'],
                        'value': result['amount']
                    }
                )

            data.update({
                'pay': re
            })

        # 根据金额、数量统计前五名产品
        sql_06 = """
             SELECT td.name as name,tb.product_id as product_id ,sum((case  when discount>0  then qty*price_unit*(discount/100) else qty*price_unit end))  as amount
            FROM public.pos_order as ta 
            left join pos_order_line as tb on ta.id=tb.order_id
            left join product_product as tc on tc.id=tb.product_id
              left join product_template as td on td.id=tc.product_tmpl_id
            where ta.date_order>='%s' and  ta.date_order<='%s' 
            and ta.slae_type='in' and (ta.state='paid' or ta.state='done')
            group by td.name,tb.product_id
            order by sum((qty*price_unit* (case  when discount>0 then discount else 1 end)))  desc
            limit 5
        """ % (start_time, end_time)
        self.env.cr.execute(sql_06)
        re1 = []
        for result in self.env.cr.dictfetchall():
            re1.append({
                'name': result['name'],
                'product_id': result['product_id'],
                'end_time': end_time,
                'start_time': start_time,
                'value': result['amount']
            }
            )
        data.update({
            'amount_limit': re1
        })

        sql_07 = """
             SELECT td.name as name,tb.product_id as product_id,sum(qty)  as qty
            FROM public.pos_order as ta 
            left join pos_order_line as tb on ta.id=tb.order_id
              left join product_product as tc on tc.id=tb.product_id
              left join product_template as td on td.id=tc.product_tmpl_id
            where ta.date_order>='%s' and  ta.date_order<='%s' 
            and ta.slae_type='in' and  (ta.state='paid' or ta.state='done')
            group by td.name,tb.product_id
            order by sum(qty)  desc
            limit 5
        """ % (start_time, end_time)
        self.env.cr.execute(sql_07)
        re2 = []
        for result in self.env.cr.dictfetchall():
            re2.append(
                {
                    'name': result['name'],
                    'product_id': result['product_id'],
                    'end_time': end_time,
                    'start_time': start_time,
                    'value': result['qty']
                }
            )

        data.update({
            'qty_limit': re2
        })

        data.update({
            'domain': {
                'in': ['&', '&', ('date_order', '>=', start_time), ('date_order', '<=', end_time),
                       ('slae_type', '=', 'in')],
                'out': ['&', '&', ('date_order', '>=', start_time), ('date_order', '<=', end_time),
                        ('slae_type', '=', 'out')],
            }
        })

        return data

    @api.model
    def search_milimit(self, start_time, end_time, name):
        # 支付方式数据穿透
        if start_time in [1, 2, 3, 4]:
            start_time, end_time = self.get_datetime(start_time)

        if name:
            journal_id = self.env['account.journal'].sudo().search([('name', '=', name), ('journal_user', '=', True)],
                                                                   limit=1).id
            domain = ['&', '&', ('date_order', '>=', start_time), ('date_order', '<=', end_time),
                      ('journal_id', '=', journal_id)]
        else:
            domain = ['&', ('date_order', '>=', start_time), ('date_order', '<=', end_time)]
        return domain

    @api.model
    def search_top(self, start_time, end_time):
        # 产品排行榜数据穿透
        if start_time in [1, 2, 3, 4]:
            start_time, end_time = self.get_datetime(start_time)
        domain = ['&', ('date_order', '>=', start_time), ('date_order', '<=', end_time)]

        return domain


class PosOrderLine(models.Model):
    _inherit = "pos.order.line"

    product_uom = fields.Many2one('product.uom', string='单位')
    refund_qty = fields.Integer(string="退货数量")

    @api.depends('price_unit', 'tax_ids', 'qty', 'discount', 'product_id')
    def _compute_amount_line_all(self):
        for line in self:
            fpos = line.order_id.fiscal_position_id
            tax_ids_after_fiscal_position = fpos.map_tax(line.tax_ids, line.product_id,
                                                         line.order_id.partner_id) if fpos else line.tax_ids
            # price = line.price_unit * ((line.discount or 0.0) / 100.0)
            if line.discount == 0:
                price = line.price_unit
            else:
                price = line.price_unit * (line.discount / 100.0)
            taxes = tax_ids_after_fiscal_position.compute_all(price, line.order_id.pricelist_id.currency_id, line.qty,
                                                              product=line.product_id, partner=line.order_id.partner_id)
            line.update({
                'price_subtotal_incl': taxes['total_included'],
                'price_subtotal': taxes['total_excluded'],
            })

    price_unit = fields.Float(string='Unit Price', digits=0)
    product_id = fields.Many2one('product.product', string='Product', domain=[('sale_ok', '=', True)], required=True,
                                 change_default=True)
    qty = fields.Float('Quantity', digits=dp.get_precision('Product Unit of Measure'), default=1)
    price_subtotal = fields.Float(compute='_compute_amount_line_all', digits=0, string='Subtotal w/o Tax')
    price_subtotal_incl = fields.Float(compute='_compute_amount_line_all', digits=0, string='Subtotal')
    discount = fields.Float(string='Discount (%)', digits=0, default=0.0)
    tax_ids = fields.Many2many('account.tax', string='Taxes', readonly=True)

    @api.onchange('qty', 'discount', 'price_unit', 'tax_ids')
    def _onchange_qty(self):
        if self.product_id:
            if not self.order_id.pricelist_id:
                raise UserError(_('You have to select a pricelist in the sale form !'))
            # price = self.price_unit * ((self.discount or 0.0) / 100.0)
            if self.discount == 0:
                price = self.price_unit
            else:
                price = self.price_unit * (self.discount / 100.0)
            self.price_subtotal = self.price_subtotal_incl = price * self.qty
            if (self.product_id.taxes_id):
                taxes = self.product_id.taxes_id.compute_all(price, self.order_id.pricelist_id.currency_id, self.qty,
                                                             product=self.product_id, partner=False)
                self.price_subtotal = taxes['total_excluded']
                self.price_subtotal_incl = taxes['total_included']

    @api.onchange('product_id')
    def _onchange_product_id(self):
        if self.product_id:
            if not self.order_id.pricelist_id:
                raise UserError(
                    _('You have to select a pricelist in the sale form !\n'
                      'Please set one before choosing a product.'))
            price = self.order_id.pricelist_id.get_product_price(
                self.product_id, self.qty or 1.0, self.order_id.partner_id)
            self._onchange_qty()
            self.price_unit = price
            self.tax_ids = self.product_id.taxes_id
            self.product_uom = self.product_id.uom_id


class PosConfig(models.Model):
    _inherit = 'pos.config'

    def compute_today(self):
        for rec in self:
            start_time = datetime.datetime.now().strftime('%Y-%m-%d 00:00:00')
            end_time = datetime.datetime.now().strftime('%Y-%m-%d 23:59:59')
            res = self.env['pos.order'].search([('date_order', '>=', start_time), ('date_order', '<=', end_time)])
            today_amount = 0.0;
            for lines in res:
                for amount_lines in lines.statement_ids:
                    today_amount += amount_lines.amount

            today_qty = self.env['pos.order'].search_count(
                [('date_order', '>=', start_time), ('date_order', '<=', end_time)])

            rec.today_amount = today_amount
            rec.today_qty = today_qty

            session = self.env['pos.session'].search([('state', '=', 'opened'),('user_id', '=',self.env.uid)],limit=1)
            rec.start_at = session.start_at

    start_at = fields.Datetime(string='上次登录日期', compute=compute_today)
    today_amount = fields.Float(string='今日销售额', compute=compute_today)
    today_qty = fields.Integer(string='今日订单数量', compute=compute_today)


class PosLoyaltyReward(models.Model):
    _inherit = 'loyalty.reward'
    _sql_constraints = [
        ('driver_id_unique', 'UNIQUE(gift_product_id)', 'Only one car can be assigned to the same employee!')
    ]
