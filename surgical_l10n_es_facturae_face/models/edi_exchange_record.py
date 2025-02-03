from odoo import models, fields
from odoo.exceptions import UserError


class EdiExchangeRecord(models.Model):
    _inherit = 'edi.exchange.record'

    def manually_exchange_send(self):
        for record in self:
            try:
                record.action_exchange_send()
            except Exception as e:
                raise UserError(f'Error sending FACe exchange id: ({record.id}). Error: {str(e)}')