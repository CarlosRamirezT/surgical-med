# -*- coding: utf-8 -*-
# from odoo import http


# class SurgicalDeliveryPackageNumber(http.Controller):
#     @http.route('/surgical_delivery_package_number/surgical_delivery_package_number', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/surgical_delivery_package_number/surgical_delivery_package_number/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('surgical_delivery_package_number.listing', {
#             'root': '/surgical_delivery_package_number/surgical_delivery_package_number',
#             'objects': http.request.env['surgical_delivery_package_number.surgical_delivery_package_number'].search([]),
#         })

#     @http.route('/surgical_delivery_package_number/surgical_delivery_package_number/objects/<model("surgical_delivery_package_number.surgical_delivery_package_number"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('surgical_delivery_package_number.object', {
#             'object': obj
#         })

