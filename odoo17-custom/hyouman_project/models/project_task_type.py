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
            
    @api.model_create_multi
    def create(self, vals_list):
        res = super().create(vals_list)

        for task in res:
            related_stage_goals = self.env['goal.goal'].search([]).filtered(lambda goal: task.stage_id in goal.related_section_ids)
            for goal in related_stage_goals:
                goal._compute_completion_percentage()
        
        return res

    def write(self, vals):
        res = super().write(vals)
        
        if 'state' in vals:
            print(vals)
            related_stage_goals = self.env['goal.goal'].search([]).filtered(lambda goal: self.stage_id in goal.related_section_ids)
            for goal in related_stage_goals:
                goal._compute_completion_percentage()
            
        return res