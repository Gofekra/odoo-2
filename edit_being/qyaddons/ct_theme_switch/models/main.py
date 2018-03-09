# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import datetime
from itertools import islice
import json
import xml.etree.ElementTree as ET
import logging
import re
import urllib2
import werkzeug.utils
import werkzeug.wrappers

import odoo
from odoo import http
from odoo import fields
from odoo.http import request
from odoo.osv.orm import browse_record

from odoo.addons.website.models.website import slug
from odoo.addons.web.controllers.main import WebClient, Binary, Home
logger = logging.getLogger(__name__)



class Theme_switch(http.Controller):
    def get_view_ids(self, xml_ids):
        ids = []
        for xml_id in xml_ids:
            if "." in xml_id:
                record_id = request.env.ref(xml_id).id
            else:
                record_id = int(xml_id)
            ids.append(record_id)
        return ids


    @http.route(['/ct_theme_switch/theme_customize'], type='json', auth="public", website=True)
    def theme_customize(self, enable, disable, get_bundle=False):
        """ enable or Disable lists of ``xml_id`` of the inherit templates """

        def set_active(ids, active):
            if ids:
                real_ids = self.get_view_ids(ids)
                request.env['ir.ui.view'].with_context(active_test=True).browse(real_ids).write({'active': active})

        set_active(disable, False)
        set_active(enable, True)

        if get_bundle:
            context = dict(request.context, active_test=True)
            return request.env["ir.qweb"]._get_asset('web.assets_frontend', options=context)
        return True