# -*- coding: utf-8 -*-
from odoo import http

# class CtProjectUf(http.Controller):
#     @http.route('/ct_project_uf/ct_project_uf/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/ct_project_uf/ct_project_uf/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('ct_project_uf.listing', {
#             'root': '/ct_project_uf/ct_project_uf',
#             'objects': http.request.env['ct_project_uf.ct_project_uf'].search([]),
#         })

#     @http.route('/ct_project_uf/ct_project_uf/objects/<model("ct_project_uf.ct_project_uf"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('ct_project_uf.object', {
#             'object': obj
#         })