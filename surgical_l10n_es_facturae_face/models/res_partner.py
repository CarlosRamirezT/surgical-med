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
        
        # using batch execution to make a commit every 50 records so we free RAM resources and module update does not freeze

        records_to_process = self.filtered(lambda partner: partner.facturae and not partner.l10n_es_facturae_customer_name)
        total_records = len(records_to_process)
        batch_counter = 0
        
        for partner in records_to_process:
            partner.l10n_es_facturae_customer_name = partner._get_facturae_format_name()
            
            batch_counter += 1
            # Every 50 records, commit to free RAM and resources.
            if batch_counter % 50 == 0 or batch_counter == total_records:
                self.env.cr.commit()

    def _get_facturae_format_name(self):
        self.ensure_one()
        return self.name[:40]

