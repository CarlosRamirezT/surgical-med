{
    "name": "Quality Control (SurgicalMed)",
    "summary": "SurgicalMed Customizations for Quality Control Enterprise Module",
    "description": """SurgicalMed Customizations for Quality Control Enterprise Module""",
    "author": "My Company",
    "website": "https://surgicalmed.es/",
    "category": "Manufacturing/Quality",
    "version": "17.0.0.1",
    "depends": ["quality_control", "helpdesk", "sign"],
    "data": [
        "security/ir.model.access.csv",

        "views/res_config_settings.xml",
        "views/quality_alert_views.xml",
        "views/quality_evaluation_supplier_criteria_views.xml",
        "views/quality_evaluation_supplier_template.xml",
        "views/quality_evaluation_supplier_views.xml",
        "views/quality_supplier_document_template_views.xml",
        "views/quality_supplier_document_views.xml",
        "views/helpdesk_ticket_views.xml",
        "views/quality_alert_stage_views.xml",
        
        "wizards/quality_action_notify_wizard_views.xml",

        "reports/quality_alert_report.xml",

        "data/quality_alert_data.xml",
    ],
}
