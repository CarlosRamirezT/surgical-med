# Copyright 2020 Tecnativa - David Vidal
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
import logging
from xml.sax.saxutils import escape

from odoo import _, api, fields, models
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class DeliveryCarrier(models.Model):
    _inherit = "delivery.carrier"

    def _prepare_gls_asm_shipping(self, picking):
        res = super(DeliveryCarrier, self)._prepare_gls_asm_shipping(picking)
        
        # update the customized values

        res["destinatario_observaciones"] = (
            picking.note and escape(picking.note) or ""
        )
        res["referencia_c"] = (
            picking.origin
            and escape(f"{picking.name}/{picking.origin}")
            or escape(picking.name),
        )  # Our unique reference

        # return updated shipping values
        
        return res
