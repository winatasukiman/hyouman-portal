# -*- coding: utf-8 -*-
###############################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#
#    Copyright (C) 2024-TODAY Cybrosys Technologies(<https://www.cybrosys.com>)
#    Author:  Cybrosys Techno Solutions(<https://www.cybrosys.com>)
#
#    You can modify it under the terms of the GNU AFFERO
#    GENERAL PUBLIC LICENSE (AGPL v3), Version 3.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU AFFERO GENERAL PUBLIC LICENSE (AGPL v3) for more details.
#
#    You should have received a copy of the GNU AFFERO GENERAL PUBLIC LICENSE
#    (AGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################
from datetime import datetime
from odoo import fields, models, _
from odoo.exceptions import ValidationError

import logging
_logger = logging.getLogger(__name__)
try:
    import asana
except ImportError:
    _logger.debug('Cannot `import asana`.')

class ProjectTask(models.Model):
    """
    Inherits the model project.task to add extra fields for the working of
    importing and exporting of the data from odoo to asana
    """
    _inherit = 'project.task'

    asana_gid = fields.Char(string='Asana GID',
                            help='Asana ID for the project record',
                            readonly=True)
    
    def action_import_stories(self):
        """
        Method button_import_stories to import the stories from asana to odoo
        """
        for record in self:
            configuration = asana.Configuration()
            configuration.access_token = self.env[
                'ir.config_parameter'].sudo().get_param(
                'asana_odoo_connector.app_token')
            api_client = asana.ApiClient(configuration)
            story_instance = asana.StoriesApi(api_client)
            
            for message in record.message_ids.filtered(lambda m: 
                m.message_type == 'comment' and
                not m.is_internal
            ):
                message.unlink()
            
            try:
                stories_response = story_instance.get_stories_for_task(record.asana_gid, {})
                for story in stories_response:
                    opts = {
                        'opt_fields': "gid,created_at,created_by,text,type,html_text",
                    }
                    story_response = story_instance.get_story(story['gid'], opts)
                    if story['type'] != 'comment':
                        continue
                    
                    date_str = False
                    if story['created_at']:
                        date_dt = datetime.strptime(story['created_at'], '%Y-%m-%dT%H:%M:%S.%fZ')
                        # Convert to string if storing in char/fields.Datetime
                        date_str = date_dt.strftime('%Y-%m-%d %H:%M:%S')
                    
                    user = False
                    if story['created_by']:
                        user = self.env['res.users'].search([
                            ('active', '=', True),
                            ('name', '=', story['created_by']['name'])
                        ])
                    
                    # Create comment record
                    self.env['mail.message'].create({
                        'model': 'project.task',
                        'body': story_response['html_text'],
                        'author_id': user.partner_id.id if user else False,
                        'message_type': 'comment',
                        'res_id': record.id,
                        'date': date_str,
                    })
            except Exception as exc:
                raise ValidationError(exc)
            else:
                return record.project_id.action_notify(True, 'Task', record.name)
            
    def open_wizard_create_fields(self):
        """
        Opens the wizard to create dynamic fields for the project task
        """
        model_id = self.env['ir.model'].sudo().search([('model', '=', 'project.task')])
        
        return {
            'type': 'ir.actions.act_window',
            'name': 'Create Dynamic Fields',
            'res_model': 'project.dynamic.fields',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_model_id': model_id.id,
                # 'default_form_view_id': self.env.ref('project.edit_project').id,
                'default_project_id': self.project_id.id,
                'default_position_field_id': 'after',
            }
        }