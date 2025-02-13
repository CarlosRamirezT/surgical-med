from odoo import models, fields


class ResCompany(models.Model):
    _inherit = "res.company"

    facturae_send_invoice_manually_to_face_on_submit = fields.Boolean(
        "Send the invoice manually to FACe", default=False
    )


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    facturae_send_invoice_manually_to_face_on_submit = fields.Boolean(
        "Send the invoice manually to FACe",
        default=False,
        related="company_id.facturae_send_invoice_manually_to_face_on_submit",
        readonly=False,
    )
