import logging

from odoo import models

_logger = logging.getLogger(__name__)


class ReturnPicking(models.TransientModel):
    _inherit = "stock.return.picking"

    def _create_returns(self):

        # execute this as sudo to avoid permission errors

        self = self.sudo()

        return super(ReturnPicking, self)._create_returns()

