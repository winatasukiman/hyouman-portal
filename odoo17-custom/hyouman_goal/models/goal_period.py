from odoo import models, fields

class GoalPeriod(models.Model):
    _name = 'goal.period'
    _description = 'Goal Period'
    _order = 'sequence, id'

    name = fields.Char(string='Period Name', required=True, help="e.g., Q3 FY25")
    sequence = fields.Integer(string='Sequence', default=10)
    active = fields.Boolean(default=True)