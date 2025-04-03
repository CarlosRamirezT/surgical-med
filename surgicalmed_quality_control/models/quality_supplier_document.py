from odoo import models, fields, api
from datetime import timedelta

class QualitySupplierDocumentTemplate(models.Model):
    _name = 'quality.supplier.document.template'
    _description = 'Quality Supplier Document Template'

    name = fields.Char(string="Template Name", required=True)
    document_line_ids = fields.One2many(
        'quality.supplier.document.template.line',
        'template_id',
        string="Document Lines"
    )


class QualitySupplierDocumentTemplateLine(models.Model):
    _name = 'quality.supplier.document.template.line'
    _description = 'Quality Supplier Document Template Line'

    template_id = fields.Many2one(
        'quality.supplier.document.template',
        string="Template",
        required=True
    )
    name = fields.Char(string="Document Name", required=True)
    description = fields.Text(string="Description")


class QualitySupplierDocument(models.Model):
    _name = 'quality.supplier.document'
    _description = 'Quality Supplier Document'

    name = fields.Char(string="Document Name", required=True)
    partner_id = fields.Many2one(
        'res.partner',
        string="Supplier",
        required=True
    )
    issue_date = fields.Date(string="Issue Date")
    expiration_date = fields.Date(string="Expiration Date")
    validity_days = fields.Integer(string="Validity Days")
    document_file = fields.Binary(string="Document File")

    @api.onchange('validity_days')
    def _onchange_validity_days(self):
        if self.issue_date and self.validity_days:
            self.expiration_date = self.issue_date + timedelta(days=self.validity_days)

    @api.onchange('expiration_date')
    def _onchange_expiration_date(self):
        if self.issue_date and self.expiration_date:
            delta = self.expiration_date - self.issue_date
            self.validity_days = delta.days


class ResPartner(models.Model):
    _inherit = 'res.partner'

    quality_document_ids = fields.One2many(
        'quality.supplier.document',
        'partner_id',
        string="Quality Documents"
    )
    document_template_id = fields.Many2one(
        'quality.supplier.document.template',
        string="Document Template"
    )

    @api.onchange('document_template_id')
    def _onchange_document_template_id(self):
        if self.document_template_id:
            self.quality_document_ids = [(5, 0, 0)]  # Clear existing lines
            for line in self.document_template_id.document_line_ids:
                self.quality_document_ids = [(0, 0, {
                    'name': line.name,
                })]

    @api.onchange('quality_document_ids')
    def _onchange_quality_document_ids(self):
        for document in self.quality_document_ids:
            if document.expiration_date and document.expiration_date < fields.Date.today():
                document.message_post(
                    body="The document '{}' has expired.".format(document.name),
                    subtype_xmlid="mail.mt_note"
                )

    def action_update_expired_documents(self):
        for partner in self:
            for document in partner.quality_document_ids:
                if document.expiration_date and document.expiration_date < fields.Date.today():
                    old_expiration_date = document.expiration_date
                    document.expiration_date = fields.Date.today() + timedelta(days=document.validity_days)
                    document.message_post(
                        body=(
                            "The document '{}' has been updated. "
                            "Old expiration date: {}. New expiration date: {}."
                        ).format(
                            document.name,
                            old_expiration_date,
                            document.expiration_date
                        ),
                        subtype_xmlid="mail.mt_note"
                    )