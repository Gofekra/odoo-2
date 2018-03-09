# -*- coding: utf-8 -*-
from lxml import etree

from odoo import api, fields, models, tools, SUPERUSER_ID, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools.safe_eval import safe_eval


class BaseConfigSettings(models.TransientModel):
    _name = 'ct_calendar.config.settings'
    _inherit = 'res.config.settings'


    @api.multi
    def _default_get_group_ids(self):
        # print 'Getting group_ids'
        if self.env['ir.values'].sudo().get_default('ct_calendar.config.settings', 'meeting_pmo_group_users'):
            return self.env['ir.values'].sudo().get_default('ct_calendar.config.settings', 'meeting_pmo_group_users')
        return []


    user_ids = fields.Many2many('res.users', string="PMO group members", translated=True,
                               default=lambda self: self._default_get_group_ids())


    @api.multi
    def set_user_ids_defaults(self):
        # print 'setting group_ids'
        # print self.group_ids.mapped('id')
        return self.env['ir.values'].sudo().set_default(
            'ct_calendar.config.settings', 'meeting_pmo_group_users', self.user_ids.mapped('id'))
