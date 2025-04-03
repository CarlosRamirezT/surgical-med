from odoo import models, fields, api

class QualityActionNotifyWizard(models.TransientModel):
    _name = 'quality.action.notify.wizard'
    _description = 'Quality Action Notify Wizard'

    quality_action_id = fields.Many2one('quality.action', string='Quality Action', required=True, readonly=True)
    user_assigned_id = fields.Many2one('res.users', string='Assigned User', required=True, readonly=True)
    message = fields.Text(string='Message', required=True)

    def action_send_notification(self):
        """Send notification to the assigned user."""
        if self.user_assigned_id and self.message:
            # Send a notification to the assigned user
            self.env['mail.message'].create({
                'subject': 'Quality Action Notification',
                'body': self.message,
                'message_type': 'notification',
                'subtype_id': self.env.ref('mail.mt_comment').id,
                'partner_ids': [(4, self.user_assigned_id.partner_id.id)],
            })
        return {'type': 'ir.actions.act_window_close'}