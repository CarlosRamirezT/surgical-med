# Copyright 2020 Creu Blanca
# @author: Enric Tobella
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.addons.component.core import Component


class AccountMoveL10nEsFacturaeListener(Component):
    _inherit = "account.move.l10n.es.facturae.listener"

    def on_post_account_move(self, records):
        # use our new method without jobs so the user works faster
        records.manually_send_invoice_to_face()
