# -*- coding: utf-8 -*-

# from odoo import models, fields, api

import pytz
import datetime
import logging


from odoo import api, fields, models, tools, SUPERUSER_ID, _
from odoo.exceptions import AccessDenied, AccessError, UserError, ValidationError
from odoo.osv import expression
from odoo.service.db import check_super
from odoo.tools import partition

_logger = logging.getLogger(__name__)


class res_users(models.Model):
    _inherit= 'res.users'

    theme_type=fields.Selection([ ('ct_dxb_home.ct_theme_default','默认风格'),('ct_dxb_home.ct_theme_blue','蓝色风格'),('ct_dxb_home.ct_theme_palm','棕色风格'),('ct_dxb_home.ct_theme_deepblue','深蓝风格'),('ct_dxb_home.ct_theme_green','绿色风格')
        ],string='主题风格',default="ct_dxb_home.ct_theme_default")



    def __init__(self, pool, cr):
        """ Override of __init__ to add access rights on notification_email_send
            and alias fields. Access rights are disabled by default, but allowed
            on some specific fields defined in self.SELF_{READ/WRITE}ABLE_FIELDS.
        """
        init_res = super(res_users, self).__init__(pool, cr)
        # duplicate list to avoid modifying the original reference
        type(self).SELF_WRITEABLE_FIELDS = list(self.SELF_WRITEABLE_FIELDS)
        type(self).SELF_WRITEABLE_FIELDS.extend(['theme_type'])
        # duplicate list to avoid modifying the original reference
        type(self).SELF_READABLE_FIELDS = list(self.SELF_READABLE_FIELDS)
        type(self).SELF_READABLE_FIELDS.extend(['theme_type'])
        return init_res

    @api.model
    def search_theme(self):
    	uid=self.env.uid
    	res=self.sudo().search([('id','=',uid)]).theme_type

    	return res

