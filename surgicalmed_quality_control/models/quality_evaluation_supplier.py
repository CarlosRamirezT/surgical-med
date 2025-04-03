from odoo import models, fields

class QualityEvaluationSupplier(models.Model):
    _name = 'quality.evaluation.supplier'
    _description = 'Supplier Evaluation'

    name = fields.Char(string='Supplier', required=True, related='partner_id.name', store=True)
    partner_id = fields.Many2one('res.partner', string='Supplier', required=True)
    address = fields.Char(string='Address', related='partner_id.contact_address', store=True)
    contact = fields.Char(string='Contact', related='partner_id.phone', store=True)
    email = fields.Char(string='Email', related='partner_id.email', store=True)
    category = fields.Char(string='Category', related='partner_id.category_id.name', store=True)