from odoo import models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    def send_to_shipper(self):

        # validate a duplicated shipping is not send to GLS
        # Sometimes when proccessing rate_and_ship methods
        # pickings are posted for a second time and a
        # error -70: albaran ya existe, raises.

        if (
            len(self) == 1
            and self.carrier_id.delivery_type == "gls_asm"
            and self.carrier_tracking_ref
        ):
            return

        super(StockPicking, self).send_to_shipper()
