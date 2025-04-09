from odoo import models, fields


class QualityPoint(models.Model):
    _inherit = "quality.point"

    measure_on = fields.Selection(
        selection_add=[
            ("lot_id", "Lot/Serial"),
        ],
        help="""Operation = One quality check is requested at the operation level.
                  Product = A quality check is requested per product.
                 Quantity = A quality check is requested for each new product quantity registered, with partial quantity checks also possible.
                 Lot/Serial = A quality check is requested for each lot/serial number registered, with partial quantity checks also possible.
                 """,
        ondelete={
            "lot_id": "set default",
        },
    )
    
    def _get_checks_values(self, products, company_id, existing_checks=False):
        point_values = super(QualityPoint, self)._get_checks_values(products, company_id, existing_checks)

        # TODO: implement this logic

        return point_values
    
