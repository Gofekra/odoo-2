# -*- coding: utf-8 -*-

import babel.dates
import time
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

import werkzeug.urls
from werkzeug.exceptions import NotFound

from odoo import http
from odoo import tools
from odoo.http import request
from odoo.tools.translate import _
from odoo.addons.website.models.website import slug


class website_event(http.Controller):
    @http.route(['/module', '/module/<path:page>'], type='http', auth="public", website=True)
    def events(self, page="sales"):
        if '.' not in page:
            page = 'ct_website_module_menu.%s' % page

        try:
            request.website.get_template(page)
        except ValueError, e:
            # page not found
            raise NotFound
        print page
        return request.render(page)
