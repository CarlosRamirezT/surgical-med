# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class surgical_delivery_package_number(models.Model):
#     _name = 'surgical_delivery_package_number.surgical_delivery_package_number'
#     _description = 'surgical_delivery_package_number.surgical_delivery_package_number'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

