from odoo import models, fields, api

class QualitySupplierDocumentTemplate(models.Model):
    _name = 'quality.supplier.document.template'
    _description = 'Quality Supplier Document Template'

    name = fields.Char(string="Template Name", required=True)
    document_line_ids = fields.One2many(
        comodel_name='quality.supplier.document.template.line',
        inverse_name='template_id',
        string="Document Lines"
    )


class QualitySupplierDocumentTemplateLine(models.Model):
    _name = 'quality.supplier.document.template.line'
    _description = 'Quality Supplier Document Template Line'

    template_id = fields.Many2one(
        comodel_name='quality.supplier.document.template',
        string="Template",
        readonly=True,
        index=True,
        auto_join=True,
        ondelete="cascade",
        check_company=True,
    )
    name = fields.Char(string="Document Name", required=True)
    description = fields.Text(string="Description")