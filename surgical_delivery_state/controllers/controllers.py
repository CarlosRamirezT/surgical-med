# -*- coding: utf-8 -*-
# from odoo import http


# class SurgicalDeliveryState(http.Controller):
#     @http.route('/surgical_delivery_state/surgical_delivery_state', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/surgical_delivery_state/surgical_delivery_state/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('surgical_delivery_state.listing', {
#             'root': '/surgical_delivery_state/surgical_delivery_state',
#             'objects': http.request.env['surgical_delivery_state.surgical_delivery_state'].search([]),
#         })

#     @http.route('/surgical_delivery_state/surgical_delivery_state/objects/<model("surgical_delivery_state.surgical_delivery_state"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('surgical_delivery_state.object', {
#             'object': obj
#         })

