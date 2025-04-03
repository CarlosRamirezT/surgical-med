from odoo import models, fields, api

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    @api.model
    def create(self, vals):
        picking = super(StockPicking, self).create(vals)
        if picking.picking_type_id.code in ['incoming', 'internal']:
            for move in picking.move_lines:
                self.env['quality.check'].create({
                    'picking_id': picking.id,
                    'product_id': move.product_id.id,
                    'product_qty': move.product_uom_qty,
                    'state': 'pending',
                })
        return picking