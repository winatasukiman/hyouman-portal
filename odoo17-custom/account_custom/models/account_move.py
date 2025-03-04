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

    # Override function
    # Add text "PAID" in the report name if the invoice has been paid
    def _get_invoice_report_filename(self, extension='pdf'):
        """ Get the filename of the generated invoice report with extension file. """
        self.ensure_one()
        result = f"{self.name.replace('/', '_')}.{extension}"
        if self.payment_state in ('paid', 'in_payment'):
            result = f"{self.name.replace('/', '_')} (PAID).{extension}"

        return result

    # Add a field that will be displayed in both unpaid/paid invoice email content
    partner_child = fields.Char('Child')
