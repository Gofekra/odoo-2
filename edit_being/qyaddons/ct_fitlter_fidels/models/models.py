# -*- coding: utf-8 -*-

from odoo import models, fields, api

class IrModelFields(models.Model):
    _inherit = 'ir.model.fields'

    cancel_filter=fields.Boolean(string="不可被过滤",default=True)


class Edit_Fidels(models.Model):
    _name = 'edit.fidels'


    @api.onchange('fields_name')
    def oncgange_fields_name(self):

        self.fields_type=self.fields_name.ttype

    @api.onchange('models_name')
    def oncgange_models_nmae(self):

        return {
            'domain':{
                'fields_name':[('model','=',self.models_name.model)]
            }
        }
    models_name = fields.Many2one('ir.model',string="调整对象",trackvisibility='onchange')
    fields_name = fields.Many2one('ir.model.fields',string="调整项",trackvisibility='onchange')
    fields_type=fields.Char(string="调整项类型")
    value_res = fields.Char(string="数值")
    condition=fields.Text(string="条件")
    sql=fields.Char(string="SQL")

    def btn_sure(self):
        domain="1=1"
        if self.condition:
            domain+=""" and %s  """ % (self.condition)
        model=(self.models_name.model).replace('.','_')
        fields=self.fields_name.name
        sql="""UPDATE %s set %s='%s'  where %s """ % (model,fields,self.value_res,domain)
        self.sql=sql
        self.env.cr.execute(sql)

class Sale_Order(models.Model):
    _inherit = 'sale.order'

    @api.model
    def fields_get(self, allfields=None, attributes=None):
        res = super(Sale_Order, self).fields_get(allfields, attributes=attributes)
        fields_to_hide = ['team_id','create_uid']
        for field in fields_to_hide:
            res[field]['selectable'] = False

        return res
