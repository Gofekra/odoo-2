# coding: utf-8


from odoo import models, fields, api


class Users(models.Model):
    _inherit = 'res.users'

    login_error_times = fields.Integer(default=0)
    is_blocked = fields.Boolean(compute='_compute_is_blocked')

    @api.multi
    def unlock_user(self):
        self.write({'login_error_times': 0})

    @api.depends('login_error_times')
    def _compute_is_blocked(self):
        t = int(self.env['ir.config_parameter'].get_param('auth_time_limit.login_error_times'))
        for r in self:
            r.is_blocked = r.login_error_times >= t
