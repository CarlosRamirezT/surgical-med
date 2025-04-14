from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class StockMove(models.Model):
    _inherit = 'stock.move'

    quality_check_id = fields.Many2one('quality.check', string="Quality Check")


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def button_validate(self):
        res = super(StockPicking, self).button_validate()
        self._create_quality_checks()
        return res
    
    def _create_quality_checks(self):
        # create quality checks for lot/serials
        quality_check_values = list()
        for picking in self:
            # get quality points that apply for this picking
            quality_points = self.env['quality.point'].sudo().search(
                [
                    ('measure_on', '=', 'lot_id'),
                    ('picking_type_ids', 'in', picking.picking_type_id.ids),
                    '|', 
                    ('product_ids', 'in', picking.move_lines.mapped('product_id').ids),
                    ('product_ids', '=', False),
                    '|',
                    ('product_category_ids', 'in', picking.move_lines.mapped('product_id.categ_id').ids),
                    ('product_category_ids', '=', False),
                ]
            )
            for quality_point in quality_points:
                for move in picking.move_lines:
                    if move.product_id in quality_point.product_ids or not quality_point.product_ids:
                        for lot in move.lot_ids:
                            # create quality check for each lot/serial
                            quality_check_values.append({
                                'product_id': move.product_id.id,
                                'lot_id': lot.id,
                                'measure_on': quality_point.measure_on,
                                'picking_id': picking.id,
                                'point_id': quality_point.id,
                                'test_type_id': quality_point.test_type_id.id,
                                'team_id': quality_point.team_id.id,
                                'note': quality_point.note,
                            })
        self.env['quality.check'].sudo().create(quality_check_values)