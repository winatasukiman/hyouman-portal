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
import json
import logging
import random
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)
try:
    import asana
except ImportError:
    _logger.debug('Cannot `import asana`.')


class ProjectProject(models.Model):
    """
    Inherits the model project.project to add extra fields and functionalities
    for the working of the odoo to asana import and export.
    """
    _inherit = 'project.project'

    asana_gid = fields.Char(string='Asana GID',
                            help='Asana ID for the project record',
                            readonly=True)
    
    def action_notify(self, success, import_type, data_name):
        """
        Method action_notify used to notify whether the import from asana is successful or not.
        """
        notification = {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Import Successful') if success is True else _('Warning'),
                'message': f'{import_type}: {data_name}' if success is True else 'Import not successful',
                'sticky': True,
                'type': 'success' if success is True else 'danger'
            }
        }
        return notification
    
    def action_import_asana_data(self):
        """
        Method action_import_asana_data to import the project data from asana to odoo
        """
        for record in self:
            configuration = asana.Configuration()
            configuration.access_token = self.env['ir.config_parameter'].sudo().get_param('asana_odoo_connector.app_token')
            api_client = asana.ApiClient(configuration)
            project_instance = asana.ProjectsApi(api_client)
            
            try:
                # Import project information
                project_response = project_instance.get_project(record.asana_gid, {})
                record.write({
                    'name': project_response['name'],
                    'description': project_response['html_notes'],
                })
                
                # Import custom fields
                CUSTOM_FIELD_TYPES = {
                    'enum': 'tags',
                    'multi_enum': 'tags',
                    'text': 'char',
                    'number': 'integer',
                    'date': 'date',
                    'people': 'many2many',
                }
                custom_fields = []
                for field in project_response['custom_field_settings']:
                    field_type = CUSTOM_FIELD_TYPES.get(field['custom_field']['type'])
                    custom_fields.append({
                        'name': field['custom_field']['gid'],
                        'type': field_type,
                        'string': field['custom_field']['name'],
                        'tags': [[option['gid'], option['name'], random.randint(1, 11)] for option in field['custom_field']['enum_options']] if field_type == 'tags' else None,
                        'selection': [[option['gid'], option['name']] for option in field['custom_field']['enum_options']] if field_type == 'selection' else None,
                        'comodel': 'hr.employee' if field_type == 'many2many' else None,
                        'view_in_cards': True,
                    })
                record.task_properties_definition = custom_fields
                
                # Import tasks
                record.action_import_tasks(
                    api_client=api_client,
                )
            except Exception as exc:
                raise ValidationError(exc)
            else:
                return record.action_notify(True, 'Project', record.name)
            
    
    def action_import_tasks(self, api_client):
        """
        Method action_import_tasks to import tasks from the asana to odoo
        """
        api_instance = asana.TasksApi(api_client)
        section_instance = asana.SectionsApi(api_client)
        opts = {}
        project_id = self.id
        asana_gid = self.asana_gid
        section_data = section_instance.get_sections_for_project(asana_gid, opts)
        for section in section_data:
            # print(section['name'])
            # opts = {
            #     'opt_fields': "actual_time_minutes,approval_status,assignee,assignee.name,assignee_section,assignee_section.name,assignee_status,completed,completed_at,completed_by,completed_by.name,created_at,created_by,custom_fields,custom_fields.asana_created_field,custom_fields.created_by,custom_fields.created_by.name,custom_fields.currency_code,custom_fields.custom_label,custom_fields.custom_label_position,custom_fields.date_value,custom_fields.date_value.date,custom_fields.date_value.date_time,custom_fields.default_access_level,custom_fields.description,custom_fields.display_value,custom_fields.enabled,custom_fields.enum_options,custom_fields.enum_options.color,custom_fields.enum_options.enabled,custom_fields.enum_options.name,custom_fields.enum_value,custom_fields.enum_value.color,custom_fields.enum_value.enabled,custom_fields.enum_value.name,custom_fields.format,custom_fields.has_notifications_enabled,custom_fields.id_prefix,custom_fields.is_formula_field,custom_fields.is_global_to_workspace,custom_fields.is_value_read_only,custom_fields.multi_enum_values,custom_fields.multi_enum_values.color,custom_fields.multi_enum_values.enabled,custom_fields.multi_enum_values.name,custom_fields.name,custom_fields.number_value,custom_fields.people_value,custom_fields.people_value.name,custom_fields.precision,custom_fields.privacy_setting,custom_fields.representation_type,custom_fields.resource_subtype,custom_fields.text_value,custom_fields.type,custom_type,custom_type.name,custom_type_status_option,custom_type_status_option.name,dependencies,dependents,due_at,due_on,external,external.data,followers,followers.name,hearted,hearts,hearts.user,hearts.user.name,html_notes,is_rendered_as_separator,liked,likes,likes.user,likes.user.name,memberships,memberships.project,memberships.project.name,memberships.section,memberships.section.name,modified_at,name,notes,num_hearts,num_likes,num_subtasks,offset,parent,parent.created_by,parent.name,parent.resource_subtype,path,permalink_url,projects,projects.name,resource_subtype,start_at,start_on,tags,tags.name,uri,workspace,workspace.name", # list[str] | This endpoint returns a resource which excludes some properties by default. To include those optional properties, set this query parameter to a comma-separated list of the properties you wish to include.
            # }
            opts = {
                'opt_fields': "gid,name,assignee,assignee.name,completed,html_notes,due_on,",
            }
            task_response = api_instance.get_tasks_for_section(section['gid'], opts)
            for task in task_response:
                task_data = api_instance.get_task(task['gid'], {'opt_fields': 'custom_fields'})
                
                # Custom fields
                custom_fields = {}
                for field in task_data['custom_fields']:
                    field_type = field['type']
                    if field_type == 'enum' and field['enum_value']:
                        custom_fields.update({
                            field['gid']: [field['enum_value']['gid']]
                        })
                    elif field_type == 'multi_enum' and field['multi_enum_values']:
                        custom_fields.update({
                            field['gid']: [value['gid'] for value in field['multi_enum_values']]
                        })
                    elif field_type == 'number' and field['number_value']:
                        custom_fields.update({
                            field['gid']: field['number_value']
                        })
                    elif field_type == 'text' and field['text_value']:
                        custom_fields.update({
                            field['gid']: field['text_value']
                        })
                
                # Prepare data
                task_assignee = False
                if task['assignee']:
                    task_assignee = self.env['res.users'].search([
                        ('name', '=', task['assignee']['name']) 
                    ])
                task_data = {
                    'name': task['name'],
                    'project_id': project_id,
                    'asana_gid': task['gid'],
                    'description': task['html_notes'],
                    'date_deadline': task['due_on'],
                    'state': '1_done' if task['completed'] is True else '01_in_progress',
                    'user_ids': [(6, 0, [task_assignee.id])] if task_assignee else False,
                    'stage_id': self.env['project.task.type'].search(
                        [('asana_gid', '=', section['gid']),
                            ('project_ids', '=', project_id)]).id,
                    'task_properties': custom_fields
                }
                # print(task['name'])
                
                task_record = self.env['project.task'].search([
                    ('asana_gid', '=', task['gid']),
                    ('project_id', '=', project_id)
                ])
                if not task_record:
                    # Create the task without child_ids
                    task_record = self.env['project.task'].create(task_data)
                else:
                    task_record.write(task_data)
                
                 # Populate the subtask
                subtask_response = api_instance.get_subtasks_for_task(task['gid'], opts)
                subtask_created_list = []
                for subtask in subtask_response:
                    subtask_assignee = False
                    if subtask['assignee']:
                        subtask_assignee = self.env['res.users'].search([
                            ('name', '=', subtask['assignee']['name']) 
                        ])
                    subtask_data = {
                        'name': subtask['name'],
                        'parent_id': task_record.id,
                        # 'project_id': project_id,
                        'asana_gid': subtask['gid'],
                        'description': subtask['html_notes'],
                        'date_deadline': subtask['due_on'],
                        'state': '1_done' if subtask['completed'] is True else '01_in_progress',
                        # 'color': 
                        'user_ids': [(6, 0, [subtask_assignee.id])] if subtask_assignee else False,
                    }
                    
                    subtask_record = self.env['project.task'].search([
                        ('asana_gid', '=', subtask['gid']),
                        ('project_id', '=', project_id)
                    ])
                    if not subtask_record:
                        subtask_record = self.env['project.task'].create(subtask_data)
                        subtask_created_list.append(subtask_record.id)
                    else:
                        subtask_record.write(subtask_data)
                        
                # Connect the subtask to the parent task using child_ids
                task_record.write({
                    'child_ids': [(6, 0, subtask_created_list)] if len(subtask_created_list) > 0 else False,
                })
                
                # Commented because taking too long
                # Import task stories (comment)
                # task_record.action_import_stories()
    

    def action_export_to_asana(self):
        """
        Method action_export_to_asana used to export the data in the odoo to
        asana
        """
        configuration = asana.Configuration()
        configuration.access_token = self.env[
            'ir.config_parameter'].sudo().get_param(
            'asana_odoo_connector.app_token')
        api_client = asana.ApiClient(configuration)
        project_instance = asana.ProjectsApi(api_client)
        workspace_gid = self.env[
            'ir.config_parameter'].sudo().get_param(
            'asana_odoo_connector.workspace_gid')
        try:
            for project in self:
                if not project.asana_gid:
                    project_body = {"data":{"name": project.name}}
                    project_response = project_instance.create_project_for_workspace(
                        project_body, workspace_gid, {})
                    project.asana_gid = project_response['gid']
                    project_gid = project_response['gid']
                    task_instance = asana.TasksApi(api_client)
                    section_instance = asana.SectionsApi(api_client)
                    for section in project.type_ids:
                        opts = {
                            'body': {"data": {'name': section.name}}
                        }
                        section_responses = section_instance.create_section_for_project(
                            project_gid, opts
                        )
                        section.asana_gid = section_responses['gid']
                    for task in project.tasks:
                        body = {"data": {'name': task.name,
                                         'workspace': workspace_gid,
                                         "projects": project_gid,
                                         "memberships": [{
                                             'project': project_gid,
                                             'section': task.stage_id.asana_gid
                                         }
                                         ]}}
                        task_instance.create_task(body,{})
        except Exception as exc:
            raise ValidationError(
                _('Please check the workspace ID or the app token')) from exc
