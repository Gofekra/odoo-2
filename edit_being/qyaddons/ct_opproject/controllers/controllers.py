# -*- coding: utf-8 -*-
from odoo import http

class Opproject(http.Controller):
    @http.route('/opproject/opproject/', auth='public')
    def index(self, **kw):
        return "Hello, world"

    @http.route('/opproject/opproject/objects/', auth='public')
    def list(self, **kw):
        return http.request.render('opproject.listing', {
            'root': '/opproject/opproject',
            'objects': http.request.env['opproject.opproject'].search([]),
        })

    @http.route('/opproject/opproject/objects/<model("opproject.opproject"):obj>/', auth='public')
    def object(self, obj, **kw):
        return http.request.render('opproject.object', {
            'object': obj
        })