# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


"""
inherit:odoo
auther:cchong

"""

# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import json

from odoo import api, models
from odoo.http import request

import odoo

class Http(models.AbstractModel):
    _inherit = 'ir.http'

    @api.model
    def get_client(self):
        return request.env['ir.ui.menu'].load_menus(request.debug)
