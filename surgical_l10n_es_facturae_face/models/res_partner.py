import logging

from odoo import api, models, fields

_logger = logging.getLogger(__name__)

class ResPartner(models.Model):
    _inherit = "res.partner"

    l10n_es_facturae_customer_name = fields.Char(
        "Customer Name for Facturae", 
        help="This name will be used when sending the Electronico Invoices to FACe. In case system record differ from FACe acceptance criteria of 40 characters limit.",
        store=True,
        compute=False
    )
    
    def _compute_l10n_es_facturae_customer_name(self):
        # if module is installing, ignore this. it is going to take too long
        if self._context.get('install_mode') or self.env.context.get('install_mode'):
            _logger.warning("Install mode detected, ignoring _compute_l10n_es_facturae_customer_name")
            return
        for partner in self.filtered(lambda partner: partner.facturae and not partner.l10n_es_facturae_customer_name):
            partner.l10n_es_facturae_customer_name = partner._get_facturae_format_name()

    def _get_facturae_format_name(self):
        self.ensure_one()
        return self.name[:40]

