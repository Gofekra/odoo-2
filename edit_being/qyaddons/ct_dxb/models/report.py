# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo import tools


# 零售流水
class PosSaleReport(models.Model):
    _name = "pos.sale.report"
    _auto = False

    date_order = fields.Datetime(string="单据时间")
    product_id = fields.Many2one('product.product', string="商品名称")
    qty = fields.Float(string="数量", digits=(16, 2))
    price_unit = fields.Float(string="单价", digits=(16, 2))
    amount_unit = fields.Float(string="金额", digits=(16, 2))
    discount = fields.Float(string="折扣(%)", digits=(16, 2))
    discount_unit = fields.Float(string="优惠金额", digits=(16, 2))
    rece_unit = fields.Float(string="应收金额", digits=(16, 2))
    pos_categ_id = fields.Many2one('pos.category', string="商品分类")
    partner_id = fields.Many2one('res.partner', string="会员")

    @api.model_cr
    def init(self):
        # self._table = sale_report
        tools.drop_view_if_exists(self._cr, 'pos_sale_report')
        self._cr.execute("""
            create view pos_sale_report as (                                 
                SELECT tb.id as id,ta.date_order,tb.product_id,tb.qty,tb.price_unit,
                tb.qty*tb.price_unit as amount_unit,tb.discount,td.pos_categ_id,ta.partner_id,
                CASE WHEN tb.discount=0 THEN 0 
                ELSE qty*tb.price_unit*(1-(tb.discount)/100) END as discount_unit,
                CASE WHEN tb.discount=0 THEN qty*tb.price_unit
                ELSE qty*tb.price_unit*((tb.discount)/100) END as rece_unit
                FROM public.pos_order as ta 
                left join pos_order_line as tb on ta.id=tb.order_id
                left join product_product as tc on tb.product_id= tc.id
                left join product_template as td on tc.product_tmpl_id=td.id
            )
        """)


# 收款流水
class PosReceivablesReport(models.Model):
    _name = "pos.receivables.report"
    _auto = False

    date_order = fields.Datetime(string="单据时间")
    name = fields.Char(string="单号")
    journal_id = fields.Many2one('account.journal', string="支付方式")
    pay_amount = fields.Float(string="支付金额", digits=(16, 2))
    return_amount = fields.Float(string="退款", digits=(16, 2))
    profit_amount = fields.Float(string="实收金额", digits=(16, 2))

    @api.model_cr
    def init(self):
        # self._table = sale_report
        tools.drop_view_if_exists(self._cr, 'pos_receivables_report')
        self._cr.execute("""
            create view pos_receivables_report as (
            SELECT Row_Number() over ( ) as id , ty.*from (
               SELECT date_order,name,journal_id, sum(amount)as pay_amount,
                  NULL as return_amount, sum(amount)as profit_amount FROM(
                      SELECT  ta.date_order,ta.name,tc.journal_id,tc.amount FROM public.pos_order as ta 
                        left join pos_order_line as tb on ta.id=tb.order_id							             
                        left join account_bank_statement_line as tc on ta.id=tc.pos_statement_id 
                        WHERE ta.slae_type='in'  and (state='paid' or state='done')
                        GROUP BY ta.name,tc.journal_id,tc.amount,ta.date_order)
                      as aa GROUP BY name,journal_id,date_order
                  UNION ALL 
                SELECT date_order, name,journal_id, NULL AS pay_amount,
                    SUM(amount)AS return_amount, SUM(amount)AS profit_amount FROM(
                    SELECT ta.date_order, ta.name,tc.journal_id,tc.amount 
                        FROM PUBLIC.pos_order AS ta 
                        LEFT JOIN pos_order_line AS tb on ta.id=tb.order_id							              
                        LEFT JOIN  account_bank_statement_line AS tc ON ta.id=tc.pos_statement_id
                        WHERE ta.slae_type='out'  AND (state='paid' OR state='done')
                        GROUP BY ta.name,tc.journal_id,tc.amount,ta.date_order
                    )AS bb GROUP BY name,journal_id,date_order
                )as ty
                  )
              """)


# 商品排行榜
class PosProductRank(models.Model):
    _name = "pos.produce.rank"
    _auto = False
    _order = "authentic_amount desc"

    date_order = fields.Datetime(string="单据时间")
    product_id = fields.Many2one('product.product', string="商品名称")
    authentic_qty = fields.Float(string="销售数量", digits=(16, 2))
    authentic_amount = fields.Float(string="实际销售额", digits=(16, 2))

    @api.model_cr
    def init(self):
        tools.drop_view_if_exists(self._cr, 'pos_produce_rank')
        self._cr.execute("""
         create view pos_produce_rank as (
              SELECT Row_Number() over ( ) as id ,ta.date_order,tb.product_id,(tb.qty )as authentic_qty, 
              CASE WHEN tb.discount=0 THEN (tb.qty*tb.price_unit) 
              ELSE (tb.qty*tb.price_unit*((tb.discount)/100)) END as authentic_amount
              FROM public.pos_order as ta 
              left join pos_order_line as tb on ta.id=tb.order_id
              WHERE ta.slae_type='in'  AND (state='paid' OR state='done')
          )
          
           """)


# 赠品统计
class PosProductRank(models.Model):
    _name = "pos.loyalty.program"
    _auto = False

    date_order = fields.Datetime(string="单据时间")
    product_id = fields.Many2one('product.product', string="商品名称")
    qty = fields.Float(string="数量", digits=(16, 2))
    reward_type = fields.Selection(string="奖励类型",
                                        selection=[('gift', '礼品'), ('discount', '折扣'), ('resale', '抵现')])
    # reward_type = fields.Selection(
    #                                (('gift', 'Gift'), ('discount', 'Discount'), ('resale', 'Resale')),
    #                                old_name='type',
    #                                required=True, help='The type of the reward')

    @api.model_cr
    def init(self):
        tools.drop_view_if_exists(self._cr, 'pos_loyalty_program')
        self._cr.execute("""
         create view pos_loyalty_program as (
         SELECT Row_Number() over ( ) as id , ty.*from (
              SELECT ta.date_order,tb.product_id,tb.qty,tc.reward_type 
              FROM public.pos_order as ta 
              left join pos_order_line as tb on ta.id=tb.order_id 
              left join loyalty_reward as tc on tb.product_id=tc.gift_product_id 
              WHERE tb.price_unit=0
               )as ty
               )

           """)
