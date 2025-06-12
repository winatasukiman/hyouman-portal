from odoo import models, fields

class GoalProgressSource(models.Model):
    _name = 'goal.progress.source'
    _description = 'Goal Progress Source'
    _order = 'sequence, id'

    name = fields.Char(string='Progress Source', required=True, help="e.g., Q3 FY25")
    code = fields.Char(required=True, help='Unique technical key')
    sequence = fields.Integer(string='Sequence', default=10)