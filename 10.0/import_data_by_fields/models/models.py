# coding: utf-8
from odoo import models, api, fields


class BaseImport(models.Model):
    _name = 'zx.base.import'
    _description = u'导入设置'
    name = fields.Many2one('ir.model', string=u'模型', required=True)
    fields = fields.Many2many('ir.model.fields', string=u'字段')
    _sql_constraints = [
        ('name_uniq', 'UNIQUE(name)', u'同一个模型不能重复')
    ]
