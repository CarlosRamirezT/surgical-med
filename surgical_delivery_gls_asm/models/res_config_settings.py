from odoo import models, fields


class ResCompany(models.Model):
    _inherit = "res.company"

    stock_force_quantities_if_no_available = fields.Boolean(
        "Force Quantities If No Available",
        default=True,
    )


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    stock_force_quantities_if_no_available = fields.Boolean(
        related="company_id.stock_force_quantities_if_no_available",
        readonly=False,
    )
