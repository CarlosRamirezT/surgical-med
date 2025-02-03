from odoo import models, fields

class AccountMove(models.Model):
    _inherit = 'account.move'

    def manually_send_invoice_to_face(self):
        for record in self:
            if record.edi_disable_auto:
                continue
            partner = record.partner_id
            if record.move_type not in ["out_invoice", "out_refund"]:
                continue
            if not partner.facturae or not partner.l10n_es_facturae_sending_code:
                continue
            backend = self.env.ref("l10n_es_facturae_face.face_backend")
            if not backend:
                continue
            exchange_type = self.env.ref("l10n_es_facturae_face.facturae_exchange_type")
            # We check fields now to raise an error to the user, otherwise the
            # error will be raising silently in the queue job.
            record.validate_facturae_fields()
            if record._has_exchange_record(exchange_type, backend):
                continue
            values = {
                "model": record._name,
                "res_id": record.id,
            }
            exchange_record = backend.create_record(
                exchange_type.code, values
            )
            exchange_record.action_exchange_generate()


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    def _get_invoice_stock_pickings(self):
        self.ensure_one()
        order_ids = self.sudo().sale_line_ids.order_id
        picking_ids = order_ids.picking_ids
        return picking_ids
    
    def _get_invoice_stock_picking_names(self):
        picking_ids = self._get_invoice_stock_pickings()
        picking_names = picking_ids and ",".join(picking_ids.mapped('name')) or False
        return picking_names
    
