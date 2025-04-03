from odoo import models, fields, api

class ResCompany(models.Model):
    _inherit = 'res.company'

    quality_alert_team_id = fields.Many2one(
        'quality.alert.team',
        string='Default Quality Alert Team',
    )
    quality_point_test_type_id = fields.Many2one(
        'quality.point.test_type',
        string='Default Quality Test Type',
    )


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    quality_alert_team_id = fields.Many2one(
        related='company_id.quality_alert_team_id',
        string='Default Quality Alert Team',
        readonly=False,
    )
    quality_point_test_type_id = fields.Many2one(
        related='company_id.quality_point_test_type_id',
        string='Default Quality Test Type',
        readonly=False,
    )