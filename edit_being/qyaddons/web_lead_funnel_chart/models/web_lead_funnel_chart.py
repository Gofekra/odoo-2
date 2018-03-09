# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and licensing details.
from odoo import api, models


class Crmleadextended(models.Model):
    _inherit = 'crm.lead'

    @api.multi
    def get_lead_stage_data(self):
        stage_ids = self.env['crm.stage'].search([])
        crm_name= []

        for stage in stage_ids:
            crm_lst = {}
            leads = self.search_count([('stage_id', '=', stage.id)])
            # crm_name.append(stage.name)
            crm_lst.update({
                'name':stage.name,
                'value':int(leads),
            })
            crm_name.append(crm_lst)
        print crm_name
        return crm_name
