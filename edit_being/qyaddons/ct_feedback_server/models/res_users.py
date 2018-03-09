# -*- coding: utf-8 -*-
from odoo import api, models, fields, SUPERUSER_ID, _
from odoo.exceptions import UserError, ValidationError
from odoo.osv import osv
import xmlrpclib
from ..wizard import wizard

class Users(models.Model):
    _inherit = 'res.users'

    # @api.multi
    # def write(self, vals):
    #     if self.login == wizard.FEEDBACK_USER_LOGIN:
    #         if not self.env.context.get('feedback_config', False):
    #             return True
    #     res = super(Users, self).write(vals)
    #     return res
    #
    # @api.multi
    # def unlink(self):
    #     if self.login == wizard.FEEDBACK_USER_LOGIN:
    #         return False
    #     res = super(Users, self).unlink()
    #     return res