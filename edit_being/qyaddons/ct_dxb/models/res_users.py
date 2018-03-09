# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError
import datetime
from dateutil.relativedelta import relativedelta
import odoo.addons.decimal_precision as dp


class PosOrder(models.Model):
    _inherit = 'res.users'