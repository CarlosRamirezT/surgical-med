{
    "name": "Envío de Facturae a FACe (Surgical Med)",
    "description": "Personalizaciones a la Facturación Electrónica Española para SurgicalMed.es",
    "summary": "Personalizaciones a la Facturación Electrónica Española para SurgicalMed.es",
    "version": "17.0.0.0.1",
    "author": "Carlos Ramírez, Surgical Med",
    "category": "Accounting & Finance",
    "website": "https://surgicalmed.es",
    "depends": [
        "l10n_es_facturae_face",
        "stock",
        "sale",
        "stock_picking_invoice_link", # get it from http://github.com/oca/stock-logistics-workflow
    ],
    "data": [
        "data/account_move_actions.xml",
        "data/edi_exchange_record_actions.xml",
        "views/res_partner.xml",
        "views/account_move_views.xml",
        "views/report_facturae.xml",
        "views/res_config_settings.xml",
    ],
    "installable": True,
    "maintainers": ["CarlosRamirezT (carlosdanielrt@gmail.com)",],
    #"post_init_hook": "post_init_hook",
}
