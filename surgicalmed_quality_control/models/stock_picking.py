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
                    ('product_ids', 'in', picking.move_line_ids.mapped('product_id').ids),
                    ('product_ids', '=', False),
                    '|',
                    ('product_category_ids', 'in', picking.move_line_ids.mapped('product_id.categ_id').ids),
                    ('product_category_ids', '=', False),
                ]
            )
            for quality_point in quality_points:
                for line in picking.move_line_ids.filtered(lambda line: line.lot_id):
                    if line.product_id in quality_point.product_ids or not quality_point.product_ids:
                        # create quality check for each lot/serial
                        # check if already exists
                        existing_quality_check = self.env['quality.check'].sudo().search([
                            ('product_id', '=', line.product_id.id),
                            ('lot_id', '=', line.lot_id.id),
                            ('point_id', '=', quality_point.id),
                        ])
                        if not existing_quality_check:
                            quality_check_values.append({
                                'product_id': line.product_id.id,
                                'lot_id': line.lot_id.id,
                                'measure_on': quality_point.measure_on,
                                'picking_id': picking.id,
                                'point_id': quality_point.id,
                                'test_type_id': quality_point.test_type_id and quality_point.test_type_id.id,
                                'team_id': quality_point.team_id and quality_point.team_id.id,
                                'note': quality_point.note,
                            })
        self.env['quality.check'].sudo().create(quality_check_values)