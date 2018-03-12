# -*- coding: utf-8 -*-
from odoo import http

# class CtFitlterFidels(http.Controller):
#     @http.route('/ct_fitlter_fidels/ct_fitlter_fidels/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/ct_fitlter_fidels/ct_fitlter_fidels/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('ct_fitlter_fidels.listing', {
#             'root': '/ct_fitlter_fidels/ct_fitlter_fidels',
#             'objects': http.request.env['ct_fitlter_fidels.ct_fitlter_fidels'].search([]),
#         })

#     @http.route('/ct_fitlter_fidels/ct_fitlter_fidels/objects/<model("ct_fitlter_fidels.ct_fitlter_fidels"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('ct_fitlter_fidels.object', {
#             'object': obj
#         })