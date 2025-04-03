from odoo import models, fields, api

class HelpdeskTicket(models.Model):
    _inherit = 'helpdesk.ticket'

    def action_create_quality_alert(self):
        self.ensure_one()
        quality_alert = self.env['quality.alert'].create({
            'name': f'Alert for Ticket {self.name}',
            'helpdesk_ticket_id': self.id,
            'description': self.description,
        })
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'quality.alert',
            'view_mode': 'form',
            'res_id': quality_alert.id,
            'target': 'current',
        }