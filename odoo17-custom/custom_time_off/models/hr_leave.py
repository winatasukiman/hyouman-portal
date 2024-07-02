from odoo import models, fields


class HolidaysRequestCustom(models.Model):
    _inherit = "hr.leave"

    delegate_employee_id = fields.Many2one('hr.employee', string='Delegate to', required=True)