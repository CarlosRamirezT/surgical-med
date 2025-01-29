from odoo import models, fields


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