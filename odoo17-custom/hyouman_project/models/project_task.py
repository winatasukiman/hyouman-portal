from odoo import models, fields


class ProjectTask(models.Model):
    _inherit = 'project.task'

    def button_open_formview_popup(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Project Task Form View Dialog',
            'res_model': 'project.task',
            'view_mode': 'form',
            'res_id': self.id,
            'target': 'new',
        }