# -*- coding: utf-8 -*-
from openerp import models, fields, api


class Res_company(models.Model):
    _inherit = 'res.company'

    def _compute_segments_count(self):
        for self in self:
            res = self.env['ir.config_parameter'].search([('key', '=', 'baidu_map_api_key')])
            if res:
                self.segments_count = res.value
            else:
                val = {
                    'key': "baidu_map_api_key",
                    'value': "1Qi3ZNnerS3VbxvZvZkOfKOZ9i18W1Oy"
                }
                self.env['ir.config_parameter'].create(val)
                self.segments_count=val['value']

    segments_count = fields.Char(compute='_compute_segments_count', string='密钥')
