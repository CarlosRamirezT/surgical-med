from datetime import timedelta
import logging

from odoo import models, fields, api, _

from odoo.fields import Datetime
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)

class AccountMove(models.Model):
    _inherit = 'account.move'

    # remove the compute from this fields, it takes way too many resources.
    # only execute this on invoice validation

    picking_ids = fields.Many2many(
        comodel_name="stock.picking",
        string="Related Pickings",
        store=True,
        compute=False,
        help="Related pickings (only when the invoice has been generated from a sale "
        "order).",
    )

    def _compute_picking_ids(self):
        # if module is installing, ignore this. it is going to take too long
        if self._context.get('install_mode') or self.env.context.get('install_mode'):
            _logger.warning("Install mode detected, ignoring _compute_picking_ids")
            return
        # override OCAs module logic to instad just mapped the pickings in the lines
        for invoice in self:
            invoice.picking_ids = invoice.mapped(
                "invoice_line_ids.picking_ids"
            )

    def manually_send_invoice_to_face(self):
        for record in self:
            if record.edi_disable_auto:
                continue

            company = record.company_id
            
            # check if customer credit notes should be send to FACe
            if record.move_type == 'out_refund' and not company.facturae_send_customer_credit_notes_to_face:
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

    def compute_facturae_fields(self):
        for invoice in self.filtered(lambda invoice: invoice.move_type == 'out_invoice'):
            invoice.company_id.partner_id._compute_l10n_es_facturae_customer_name()
            invoice.partner_id._compute_l10n_es_facturae_customer_name()
            invoice.invoice_line_ids._compute_picking_ids()
            invoice._compute_picking_ids()

    def action_post(self):
        # first set the required fields if not set
        # instead of computing them to consume too much ram
        self.compute_facturae_fields()
        return super(AccountMove, self).action_post()
    
    def button_draft(self):
        res = super(AccountMove, self).button_draft()
        self.compute_facturae_fields()
        return res
    
    @api.model_create_multi
    def create(self, vals_list):
        invoice_ids = super(AccountMove, self).create(vals_list)
        invoice_ids.compute_facturae_fields()
        return invoice_ids

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    picking_ids = fields.Many2many(
        comodel_name="stock.picking",
        string="Related Pickings",
        store=True,
        compute=False,
        help="Related pickings (only when the invoice has been generated from a sale "
        "order).",
        readonly=False,
    )

    def _compute_picking_ids(self):
        # if module is installing, ignore this. it is going to take too long
        if self._context.get('install_mode') or self.env.context.get('install_mode'):
            _logger.warning("Install mode detected, ignoring _compute_picking_ids")
            return
        # # Filtramos las facturas (líneas) que no tienen pickings asignados.
        for line in self.filtered(lambda line: not line.picking_ids):
            line.picking_ids = line.mapped("move_line_ids.picking_id") or line._get_invoice_stock_pickings_from_sale_order()

    def _get_invoice_stock_pickings_from_sale_order(self):
        self.ensure_one()
        self = self.sudo()
        partner_id = self.move_id.partner_shipping_id or self.move_id.partner_id
        picking_ids = self.env['stock.picking'].sudo().search([
            ('picking_type_code', '=', 'outgoing'),
            ('state', 'in', ('confirmed', 'assigned', 'done')),
            ('origin', '=', self.sale_line_ids.order_id.name),
            ('partner_id', '=', partner_id.id),
            ('invoice_ids', '=', False),
        ])
        return picking_ids
    
    def get_invoice_stock_picking_names(self):
        # try and get the pickings associated to this invoice when created from sales order
        # and if no pickings are found try and get them from a sales order search.
        # ensure all the pickings are added
        self._compute_picking_ids()
        picking_names = self.picking_ids and ",".join(self.picking_ids.mapped('name')) or ''
        return picking_names
    
