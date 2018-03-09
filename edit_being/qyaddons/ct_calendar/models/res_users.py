# -*- coding: utf-8 -*-
from lxml import etree

from odoo import api, fields, models, tools, SUPERUSER_ID, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools.safe_eval import safe_eval


class Users(models.Model):
    _inherit = 'res.users'

    ct_config_id = fields.Many2one('res.users', ondelete='set null')