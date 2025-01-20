# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class surgical_delivery_state(models.Model):
#     _name = 'surgical_delivery_state.surgical_delivery_state'
#     _description = 'surgical_delivery_state.surgical_delivery_state'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

