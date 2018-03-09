# -*- coding: utf-8 -*-
from odoo import http

# class CtFeedbackServer(http.Controller):
#     @http.route('/ct_feedback_server/ct_feedback_server/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/ct_feedback_server/ct_feedback_server/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('ct_feedback_server.listing', {
#             'root': '/ct_feedback_server/ct_feedback_server',
#             'objects': http.request.env['ct_feedback_server.ct_feedback_server'].search([]),
#         })

#     @http.route('/ct_feedback_server/ct_feedback_server/objects/<model("ct_feedback_server.ct_feedback_server"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('ct_feedback_server.object', {
#             'object': obj
#         })