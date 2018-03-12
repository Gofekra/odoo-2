# -*- coding: utf-8 -*-
from odoo import models,fields,api
to_removes = [
    'procurement.order',
    'purchase.order.line',
    'purchase.order',
    'stock.quant',
    'stock.move',
    'stock.pack.operation',
    'stock.picking',
    'stock.inventory.line',
    'stock.inventory',
    'stock.quant.package',
    'stock.quant.move.rel',
    'stock.production.lot',
    'stock.fixed.putaway.strat',
    'mrp.production.workcenter.line',
    'mrp.production',
    'mrp.production.product.line',
    'sale.order.line',
    'sale.order',
    'pos.order.line',
    'pos.order',
    'account.voucher.line',
    'account.voucher',
    'account.invoice',
    'account.partial.reconcile',
    'account.move',
]


class ClearData(models.Model):
    _name = 'clear.data'

    data_type=fields.Selection([
        ('1','供应链业务'),
        ('2','自定义')
    ],string="数据类型",help="供应链业务：采购、销售、库存、物料、POS、会计",default='2')
    models_model=fields.Many2many('ir.model',string="基础模型",required=True)
    description =fields.Char(string="原因",required=True)


    @api.multi
    def commit_clear_data(self):
        self.ensure_one()
        models_data=[]
        for models in  self.models_model:
            models_data.append(models.model)

        try:
            for obj_name in models_data:
                obj = self.pool.get(obj_name)
                if obj and obj._table_exist:
                    sql = "delete from % s"  % obj._table
                    self.env.cr.execute(sql)
        except Exception,e:
            raise Warning(e)


    @api.onchange('data_type')
    def onchange_data_type(self):
        self.models_model=''
        if self.data_type=='1':
            models_date=to_removes
            models_model=[]
            for models in models_date:
                obj = self.env['ir.model'].sudo().search([('model','=',models)])
                if obj:
                    models_model.append(obj.id)
            self.models_model=[(6,0,models_model)]


