# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


"""
inherit:Gavin
auther:cchong

"""

import logging

from odoo.http import request
from odoo import api,models


_logger = logging.getLogger(__name__)

def get_view_ids(xml_ids):
    ids = []
    for xml_id in xml_ids:
    	ids.append(request.env.ref('ct_pos_home.'+xml_id).id)        
    return ids
def set_active(ids, active):
    if ids:
        real_ids = get_view_ids(ids)
        request.env['ir.ui.view'].sudo().with_context(active_test=True).browse(real_ids).write({'active': active})

class res_users(models.Model):
    _inherit= 'res.users'

    @api.model
    def search_theme(self):
        uid=self.env.uid

        if 'theme_type' not in self.sudo().search([('id','=',uid)]):
            return False

        return self.sudo().search([('id', '=', uid)]).theme_type
            


    @api.model
    def setup_theme(self,enable,disable,get_bundle=False):

        set_active(disable, False)
        set_active(enable, True)

        if get_bundle:
            context = dict(request.context, active_test=True)
            return request.env["ir.qweb"].sudo()._get_asset('point_of_sale.assets', options=context)
        return True

