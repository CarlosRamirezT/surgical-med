from odoo import models, fields, api

class QualityAction(models.Model):
    _name = 'quality.action'
    _description = 'Improvement Actions'

    name = fields.Char(string='Action Number', required=True)
    action_type = fields.Selection(
        [
            ('type1', 'Type 1'),
            ('type2', 'Type 2'),
            ('type3', 'Type 3'),
        ],
        string='Action',
        required=True,
    )
    user_assigned_id = fields.Many2one(
        'res.users', string='Responsible', required=True
    )
    date_due = fields.Date(string='Due Date', required=True)
    date_start = fields.Datetime(string='Start Date')
    date_end = fields.Datetime(string='End Date')
    state = fields.Selection(
        [
            ('pending', 'Pending'),
            ('in_progress', 'In Progress'),
            ('closed', 'Closed'),
            ('review', 'Review'),
            ('validated', 'Validated'),
        ],
        string='Status',
        default='pending',
        required=True,
    )
    user_closed_id = fields.Many2one('res.users', string='Closed By')
    date_closed = fields.Datetime(string='Closed On')
    user_validated_id = fields.Many2one('res.users', string='Validated By')
    date_validated = fields.Datetime(string='Validated On')