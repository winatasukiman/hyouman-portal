from odoo import models, fields

class GoalSection(models.Model):
    _name = 'goal.section'
    _description = 'Goal Section'
    _order = 'sequence, id'

    name = fields.Char(string='Section Name', required=True, help="e.g., Company Goals, Marketing Team")
    sequence = fields.Integer(string='Sequence', default=10)
    active = fields.Boolean(default=True)