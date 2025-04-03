from odoo import models, fields 


class QualityAlertType(models.Model):
    _name = "quality.alert.type"
    _description = "Quality Alert Type"

    name = fields.Char(
        string="Name",
        required=True,
        help="Name of the quality alert type.",
    )
    description = fields.Text(
        string="Description",
        help="Description of the quality alert type.",
    )
    active = fields.Boolean(
        string="Active",
        default=True,
        help="Indicates if the quality alert type is active.",
    )