{
    "name": "Quality Control (SurgicalMed)",
    "summary": "SurgicalMed Customizations for Quality Control Enterprise Module",
    "description": """SurgicalMed Customizations for Quality Control Enterprise Module""",
    "author": "My Company",
    "website": "https://surgicalmed.es/",
    "category": "Manufacturing/Quality",
    "version": "17.0.0.1",
    "depends": ["quality_control"],
    "data": [
        "security/ir.model.access.csv",
        "views/quality_alert_views.xml",
        "views/quality_evaluation_supplier_criteria_views.xml",
        "views/quality_evaluation_supplier_template.xml",
        "views/quality_evaluation_supplier_views.xml",
        "views/quality_supplier_document_template_views.xml",
    ],
}
