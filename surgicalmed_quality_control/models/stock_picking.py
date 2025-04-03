from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

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

    def button_validate(self):
        for picking in self:
            pending_checks = self.env['quality.check'].search([
                ('picking_id', '=', picking.id),
                ('state', '!=', 'validated')  # Cambia 'validated' según el estado que represente validado
            ])
            if pending_checks:
                pending_products = '\n'.join(pending_checks.mapped('product_id.display_name'))
                raise ValidationError(_(
                    "No se puede validar el picking porque los siguientes productos tienen quality checks pendientes:\n\n%s"
                ) % pending_products)
        return super(StockPicking, self).button_validate()