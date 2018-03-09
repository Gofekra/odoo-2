# -*- coding: utf-8 -*-
from odoo import http

# class CtClearData(http.Controller):
#     @http.route('/ct_clear_data/ct_clear_data/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/ct_clear_data/ct_clear_data/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('ct_clear_data.listing', {
#             'root': '/ct_clear_data/ct_clear_data',
#             'objects': http.request.env['ct_clear_data.ct_clear_data'].search([]),
#         })

#     @http.route('/ct_clear_data/ct_clear_data/objects/<model("ct_clear_data.ct_clear_data"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('ct_clear_data.object', {
#             'object': obj
#         })