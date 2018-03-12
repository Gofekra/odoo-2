# -*- coding: utf-8 -*-
from odoo import http

# class CtQingjia(http.Controller):
#     @http.route('/ct_qingjia/ct_qingjia/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/ct_qingjia/ct_qingjia/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('ct_qingjia.listing', {
#             'root': '/ct_qingjia/ct_qingjia',
#             'objects': http.request.env['ct_qingjia.ct_qingjia'].search([]),
#         })

#     @http.route('/ct_qingjia/ct_qingjia/objects/<model("ct_qingjia.ct_qingjia"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('ct_qingjia.object', {
#             'object': obj
#         })