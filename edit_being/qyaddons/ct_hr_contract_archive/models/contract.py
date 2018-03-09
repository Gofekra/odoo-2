#-*- coding:utf-8 -*-
from odoo import api, fields, models, tools
import datetime
class ContractArchive(models.Model):
    _inherit = 'hr.contract'

    dimission_ok = fields.Boolean(string='已离职',default = False)
    dimission_date=fields.Datetime(string='离职时间')


    @api.onchange('dimission_date')
    def _onchange_equipment(self,dimission_date):
        self.write({'date_end': dimission_date})
