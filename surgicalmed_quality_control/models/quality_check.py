from odoo import models, fields


class QualityCheck(models.Model):
    _inherit = "quality.check"

    measure_on = fields.Selection(
        selection_add=[
            ("lot_id", "Lot/Serial"), 
        ],
        help="""Operation = One quality check is requested at the operation level.
                Product = A quality check is requested per product.
                Quantity = A quality check is requested for each new product quantity registered, with partial quantity checks also possible.
                Lot/Serial = A quality check is requested for each lot/serial number registered, with partial quantity checks also possible.
            """
    )
    lot_id = fields.Many2one(
        "stock.production.lot",
        string="Lot/Serial Number",
        check_company=True,
        help="Lot/Serial number of the product.",
    )