# -*- coding: utf-8 -*-
from odoo import http

# class CtFeedbackClient(http.Controller):
#     @http.route('/ct_feedback_client/ct_feedback_client/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/ct_feedback_client/ct_feedback_client/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('ct_feedback_client.listing', {
#             'root': '/ct_feedback_client/ct_feedback_client',
#             'objects': http.request.env['ct_feedback_client.ct_feedback_client'].search([]),
#         })

#     @http.route('/ct_feedback_client/ct_feedback_client/objects/<model("ct_feedback_client.ct_feedback_client"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('ct_feedback_client.object', {
#             'object': obj
#         })