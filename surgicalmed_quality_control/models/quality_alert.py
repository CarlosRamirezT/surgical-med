from odoo import models, fields, api


class QualityAlert(models.Model):
    _inherit = "quality.alert"

    date = fields.Date(
        string="Date",
        required=True,
        default=fields.Date.context_today,
        help="Date of the alert.",
    )
    notified = fields.Boolean(
        string="Notified",
        default=False,
        help="Indicates if the alert has been notified.",
    )
    picking_id = fields.Many2one("stock.picking", "Picking", check_company=True)
    default_code = fields.Char(
        string="Default Code",
        related="product_id.default_code",
        store=True,
        readonly=True,
    )
    identified_hazard = fields.Char(
        string="Identified Hazard",
        help="Identified hazard of the alert.",
    )
    potential_impact = fields.Selection(
        [
            ("low", "Low"),
            ("medium", "Medium"),
            ("high", "High"),
        ],
        string="Potential Impact",
        help="Potential impact of the alert.",
    )
    alert_type_id = fields.Many2one(
        "quality.alert.type",
        string="Alert Type",
        help="Type of the quality alert.",
    )
    helpdesk_ticket_id = fields.Many2one(
        "helpdesk.ticket",
        string="Helpdesk Ticket",
        help="Related helpdesk ticket for this quality alert.",
    )

    # risk classification fields
    
    risk_classification = fields.Selection(
        [
            ("minor", "Minor"),
            ("major", "Major"),
            ("critical", "Critical"),
        ],
        string="Classification",
        help="Classification → Selection:\n"
             "1. Minor: Does not affect safety or performance.\n"
             "2. Major: May affect safety, performance, or regulatory compliance.\n"
             "3. Critical: Represents a serious incident, requires notification to authorities.",
    )
    
    # risk evaluation fields

    risk_probability = fields.Selection(
        [
            ("low", "1 - Low"),
            ("medium", "2 - Medium"),
            ("high", "3 - High"),
        ],
        string="Probability",
        help="Probability of the alert.",
    )
    risk_severity = fields.Selection(
        [
            ("low", "1 - Low"),
            ("medium", "2 - Medium"),
            ("high", "3 - High"),
        ],
        string="Severity",
        help="Severity of the alert.",
    )
    risk_level = fields.Selection(
        [
            ("low", "Low"),
            ("medium", "Medium"),
            ("high", "High"),
            ("none", "N/A"),
        ],
        string="Risk Level",
        help="Risk level of the alert.",
        compute="_compute_risk_level",
        store=True,
    )

    user_closed_id = fields.Many2one('res.users', 'Closed By', tracking=True)
    user_validated_id = fields.Many2one('res.users', 'Validated By', tracking=True)
    date_validated = fields.Datetime("Date Validated", tracking=True)

    can_edit_admin_fields = fields.Boolean("Can edit admin fields in quality alerts?", compute="_compute_can_edit_admin_fields")

    def _compute_can_edit_admin_fields(self):
        self.write({'can_edit_admin_fields': self.env.user.has_group("quality.group_quality_manager")})

    @api.depends("risk_probability", "risk_severity")
    def _compute_risk_level(self):
        risk_probability_value = {
            "low": 1,
            "medium": 2,
            "high": 3,
        }
        risk_severity_value = {
            "low": 1,
            "medium": 2,
            "high": 3,
        }
        for record in self:
            probability = record.risk_probability
            severity = record.risk_severity
            if probability and severity:
                risk_level_value = risk_probability_value[probability] + risk_severity_value[severity]
                if 0 <= risk_level_value <= 2:
                    record.risk_level = "low"
                elif 3 <= risk_level_value <= 5:
                    record.risk_level = "medium"
                elif 6 <= risk_level_value <= 9:
                    record.risk_level = "high"
            else:
                record.risk_level = "none"

    @api.onchange("stage_id")
    def _onchange_stage_id(self):
        for alert in self.filtered(lambda x: x.stage_id):
            if alert.stage_id.done and not alert.user_closed_id:
                alert.user_closed_id = alert.env.user.id
                alert.date_close = fields.Datetime.now()
            elif alert.stage_id.validated and not alert.user_validated_id:
                alert.user_validated_id = alert.env.user.id
                alert.date_validated = fields.Datetime.now()


class QualityAlertStage(models.Model):
    _inherit = 'quality.alert.stage'

    validated = fields.Boolean("Validated by a supervisor")
