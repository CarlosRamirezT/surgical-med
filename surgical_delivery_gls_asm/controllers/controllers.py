# -*- coding: utf-8 -*-
# from odoo import http


# class SurgicalDeliveryGlsAsm(http.Controller):
#     @http.route('/surgical_delivery_gls_asm/surgical_delivery_gls_asm', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/surgical_delivery_gls_asm/surgical_delivery_gls_asm/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('surgical_delivery_gls_asm.listing', {
#             'root': '/surgical_delivery_gls_asm/surgical_delivery_gls_asm',
#             'objects': http.request.env['surgical_delivery_gls_asm.surgical_delivery_gls_asm'].search([]),
#         })

#     @http.route('/surgical_delivery_gls_asm/surgical_delivery_gls_asm/objects/<model("surgical_delivery_gls_asm.surgical_delivery_gls_asm"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('surgical_delivery_gls_asm.object', {
#             'object': obj
#         })

