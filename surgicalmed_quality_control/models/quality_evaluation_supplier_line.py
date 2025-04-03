from odoo import models, fields, api

class QualityEvaluationSupplierTemplateCriteria(models.Model):
    _name = 'quality.evaluation.supplier.template.line'
    _description = 'Quality Evaluation Supplier Template Line'

    evaluation_id = fields.Many2one(
        comodel_name='quality.evaluation.supplier',
        string='Supplier Evaluation',
        readonly=True,
        index=True,
        auto_join=True,
        ondelete="cascade",
        check_company=True,
    )
    template_id = fields.Many2one(
        'quality.evaluation.supplier.template',
        string='Evaluation Template',
        readonly=True,
        index=True,
        auto_join=True,
        ondelete="cascade",
        check_company=True,
)
    criteria_id = fields.Many2one(
        'quality.evaluation.supplier.criteria',
        string='Criteria',
        required=True
    )
    weight = fields.Float(string='Weight (%)', required=True)
    evaluation = fields.Integer(string='Evaluation (0-100)', required=True)
    score = fields.Float(string='Score', compute='_compute_score', store=True)
    description = fields.Text(string='Description')
    evaluation_method = fields.Text(string='How to Evaluate')

    @api.depends('weight', 'evaluation')
    def _compute_score(self):
        for record in self:
            record.score = (record.weight * record.evaluation) / 100

    @api.onchange('criteria_id')
    def _onchange_criteria_id(self):
        if self.criteria_id and not self.weight:
            self.weight = self.criteria_id.weight

class QualityEvaluationSupplierTemplateCriteria(models.Model):
    _name = 'quality.evaluation.supplier.criteria'
    _description = 'Quality Evaluation Supplier Criteria'

    name = fields.Char(string='Criteria', required=True)
    description = fields.Text(string='Description')
    evaluation_method = fields.Text(string='How to Evaluate')
    weight = fields.Float(string='Weight (%)', required=True)