from odoo import fields, models


class AccountMove(models.Model):
    _inherit = 'account.move'

    # Override function to change the invoice mail template
    def _get_mail_template(self):
        """
        :return: the correct mail template based on the current move type
        """
        return (
            'account.email_template_edi_credit_note'
            if all(move.move_type == 'out_refund' for move in self)
            else 'account_custom.hyouman_email_template_edi_invoice'
        )
