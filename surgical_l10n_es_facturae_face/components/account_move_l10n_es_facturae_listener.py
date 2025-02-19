# Copyright 2020 Creu Blanca
# @author: Enric Tobella
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.addons.component.core import Component


class AccountMoveL10nEsFacturaeListener(Component):
    _inherit = "account.move.l10n.es.facturae.listener"

    def on_post_account_move(self, records):
        # use our new method without jobs so the user works faster
        for record in records:

            company = record.company_id
            
            # check if customer credit notes should be send to FACe
            if record.move_type == 'out_refund' and not company.facturae_send_customer_credit_notes_to_face:
                continue

            if record.facturae_send_invoice_manually_to_face_on_submit:

                records.manually_send_invoice_to_face()

            else:
                
                if record.edi_disable_auto:
                    continue
                partner = record.partner_id
                if record.move_type not in ["out_invoice", "out_refund"]:
                    continue
                if not partner.facturae or not partner.l10n_es_facturae_sending_code:
                    continue
                backend = self._get_backend(record)
                if not backend:
                    continue
                exchange_type = self.env.ref("l10n_es_facturae_face.facturae_exchange_type")
                # We check fields now to raise an error to the user, otherwise the
                # error will be raising silently in the queue job.
                record.validate_facturae_fields()
                if record._has_exchange_record(exchange_type, backend):
                    continue
                exchange_record = backend.create_record(
                    exchange_type.code, self._get_exchange_record_vals(record)
                )
                exchange_record.with_delay().action_exchange_generate()

