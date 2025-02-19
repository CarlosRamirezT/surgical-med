from odoo import models, fields


class ResCompany(models.Model):
    _inherit = "res.company"

    facturae_send_invoice_manually_to_face_on_submit = fields.Boolean(
        "Send the invoice manually to FACe", default=False
    )
    facturae_send_customer_credit_notes_to_face = fields.Boolean(
        "Send Customer Credit Notes to FACe", default=False
    )


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    facturae_send_invoice_manually_to_face_on_submit = fields.Boolean(
        "Send the invoice manually to FACe",
        default=False,
        related="company_id.facturae_send_invoice_manually_to_face_on_submit",
        readonly=False,
    )
    facturae_send_customer_credit_notes_to_face = fields.Boolean(
        "Send Customer Credit Notes to FACe",
        default=False,
        related="company_id.facturae_send_customer_credit_notes_to_face",
        readonly=False,
    )
