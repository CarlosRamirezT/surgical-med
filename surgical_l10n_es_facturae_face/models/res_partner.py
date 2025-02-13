from odoo import api, models, fields


class ResPartner(models.Model):
    _inherit = "res.partner"

    l10n_es_facturae_customer_name = fields.Char(
        "Customer Name for Facturae", 
        help="This name will be used when sending the Electronico Invoices to FACe. In case system record differ from FACe acceptance criteria of 40 characters limit.",
        compute="_compute_l10n_es_facturae_customer_name",
        store=True
    )
    
    def _compute_l10n_es_facturae_customer_name(self):
        for partner in self.filtered(lambda partner: partner.facturae and not partner.l10n_es_facturae_customer_name):
            partner.l10n_es_facturae_customer_name = partner._get_facturae_format_name()

    def _get_facturae_format_name(self):
        self.ensure_one()
        return self.name[:40]

