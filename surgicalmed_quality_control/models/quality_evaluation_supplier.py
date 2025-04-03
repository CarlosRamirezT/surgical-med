from odoo import models, fields, api

class QualityEvaluationSupplier(models.Model):
    _name = 'quality.evaluation.supplier'
    _description = 'Quality Evaluation Supplier'

    supplier_id = fields.Many2one(
        'res.partner',
        string='Supplier',
        required=True,
        domain=[('supplier_rank', '>', 0)]
    )
    template_id = fields.Many2one(
        'quality.evaluation.supplier.template',
        string='Evaluation Template',
        required=True
    )
    evaluation_date = fields.Date(string='Evaluation Date', default=fields.Date.context_today, required=True)
    total_score = fields.Float(string='Total Score', compute='_compute_total_score', store=True)
    # line_ids = fields.One2many(
    #     'quality.evaluation.supplier.line',
    #     'evaluation_id',
    #     string='Evaluation Lines'
    # )
    state = fields.Selection(
        [
            ('draft', 'Draft'),
            ('in_progress', 'In Progress'),
            ('done', 'Done'),
            ('cancelled', 'Cancelled')
        ],
        string='Status',
        default='draft',
        required=True
    )

    @api.depends('line_ids.score')
    def _compute_total_score(self):
        for record in self:
            record.total_score = sum(record.line_ids.mapped('score'))

    @api.onchange('template_id')
    def _onchange_template_id(self):
        if self.state == 'draft' and self.template_id:
            self.line_ids = [(5, 0, 0)]  # Clear existing lines
            self.line_ids = [
                (0, 0, {
                    'criteria_id': line.criteria_id.id,
                    'weight': line.weight,
                    'evaluation': 0,  # Default evaluation to 0
                }) for line in self.template_id.line_ids
            ]

    def action_start(self):
        for record in self:
            if record.state == 'draft':
                record.state = 'in_progress'

    def action_done(self):
        for record in self:
            if record.state == 'in_progress':
                record.state = 'done'

    def action_cancel(self):
        for record in self:
            if record.state in ['draft', 'in_progress']:
                record.state = 'cancelled'

    def action_reset_to_draft(self):
        for record in self:
            if record.state in ['cancelled', 'done']:
                record.state = 'draft'


class QualityEvaluationSupplierTemplate(models.Model):
    _name = 'quality.evaluation.supplier.template'
    _description = 'Quality Evaluation Supplier Template'

    name = fields.Char(string='Evaluation Matrix', required=True)
    # line_ids = fields.One2many(
    #     'quality.evaluation.supplier.template.line',
    #     'template_id',
    #     string='Criteria'
    # )
    active = fields.Boolean(string='Active', default=True)

    def action_activate(self):
        for record in self:
            record.active = True

    def action_deactivate(self):
        for record in self:
            record.active = False
