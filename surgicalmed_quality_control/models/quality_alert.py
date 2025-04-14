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
    date_validated = fields.Date("Date Validated")

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


