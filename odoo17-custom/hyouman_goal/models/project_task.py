from odoo import api, models


class ProjectTask(models.Model):
    _inherit = 'project.task'
    
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