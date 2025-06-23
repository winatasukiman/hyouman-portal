# See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class ProjectProject(models.Model):
    _inherit = 'project.project'

    members_ids = fields.Many2many('res.users', 'project_user_rel', 'project_id',
                                   'user_id', 'Project Members', help="""Project's
                               members are users who can have an access to
                               the tasks related to this project."""
                                   )
    team_id = fields.Many2one('crm.team', "Project Team",
                              domain=[('type_team', '=', 'project')])

    @api.onchange('team_id')
    def _get_team_members(self):
        self.update({"members_ids": [(6, 0, self.team_id.team_members_ids.ids)]})
    
    def write(self, vals):
        res = False
        if 'team_id' or 'members_ids' in vals:
            # Current members to unsubscribe
            members_without_current_user = [
                id for id in self.members_ids.partner_id.ids 
                if id != self.env.user.partner_id.id
            ]
            # print(len(members_without_current_user), len(self.members_ids.partner_id.ids))
            self.message_unsubscribe(partner_ids=members_without_current_user)
            self.message_subscribe(partner_ids=[self.env.user.partner_id.id])
            
            # Trigger write on members_ids to update the partner_ids
            res = super(ProjectProject, self).write(vals)
            
            # New members to subscribe
            self.message_subscribe(partner_ids=self.browse(self.id).members_ids.partner_id.ids)
            
        else:
            res = super(ProjectProject, self).write(vals)
            
        return res
