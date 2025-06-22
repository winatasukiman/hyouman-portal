from odoo import api, fields, models


class ProjectTask(models.Model):
    _inherit = 'project.task.type'
    
    task_count = fields.Integer("Task Count", compute='_compute_task_count')
    done_task_count = fields.Integer("Done tasks Count", compute='_compute_task_count')
    
    def _compute_task_count(self):
        for record in self:
            tasks = self.env['project.task'].search([('stage_id', '=', record.id)])
            record.task_count = len(tasks)
            record.done_task_count = len(tasks.filtered(lambda t: t.state in ['1_done']))