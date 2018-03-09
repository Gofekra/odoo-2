# -*- coding: utf-8 -*-
from openerp import models, fields, api


class Event_Ex(models.Model):
    _inherit = 'event.event'

    def _compute_segments_count(self):
        for self in self:
            res = self.env['ir.config_parameter'].search([('key', '=', 'baidu_map_api_key')])
            print res.value
            if res:
                self.segments_count = res.value
            else:
                val = {
                    'key': "baidu_map_api_key",
                    'value': "1Qi3ZNnerS3VbxvZvZkOfKOZ9i18W1Oy"
                }
                self.env['ir.config_parameter'].create(val)
                self.segments_count=val['value']

    event_phone = fields.Char('活动热线')
    segments_count = fields.Char(compute='_compute_segments_count', string='密钥')