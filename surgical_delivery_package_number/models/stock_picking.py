from odoo import models, fields
from odoo.exceptions import UserError
from odoo.tools.float_utils import float_compare, float_is_zero, float_round

class StockPicking(models.Model):
    _inherit = "stock.picking"

    number_of_packages = fields.Integer(
        string="Number of Packages",
        default=1,
        copy=False,
        readonly=False,
        related="correos_express_number_package",
    )
    correos_express_number_package = fields.Integer(
        "Correos Express Number Packages", copy=False
    )
