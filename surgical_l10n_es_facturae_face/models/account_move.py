from datetime import timedelta

from odoo import models, fields, api

from odoo.fields import Datetime

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

    picking_ids = fields.Many2many(
        comodel_name="stock.picking",
        string="Related Pickings",
        store=True,
        compute="_compute_picking_ids",
        help="Related pickings (only when the invoice has been generated from a sale "
        "order).",
    )

    @api.depends("move_line_ids")
    def _compute_picking_ids(self):
        for invoice in self:
            invoice.picking_ids = invoice.mapped(
                "move_line_ids.picking_id"
            )

    def get_delivery_note_numbers(self):
        picking_names = self.picking_ids and ",".join(self.picking_ids.mapped('name')) or ''
        return picking_names
    
