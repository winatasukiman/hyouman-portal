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
import logging
import random
import requests
from datetime import datetime
from odoo import fields, models, _
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)
try:
    import asana
except ImportError:
    _logger.debug('Cannot `import asana`.')


def action_notify(success):
    """
    Method action_notify used to notify whether the connection to the asana is
    successful or not.
    """
    notification = {
        'type': 'ir.actions.client',
        'tag': 'display_notification',
        'params': {
            'title': _('Connection successful!') if success is True else _(
                'Connection not successful!'),
            'message': 'Connection to Asana is successful.' if success is True else 'Connection to Asana is not successful.',
            'sticky': True,
            'type': 'success' if success is True else 'danger'
        }
    }
    return notification

def action_notify_import(success):
    """
    Method action_notify used to notify whether the connection to the asana is
    successful or not.
    """
    notification = {
        'type': 'ir.actions.client',
        'tag': 'display_notification',
        'params': {
            'title': _('Import successful!') if success is True else _(
                'Import not successful!'),
            'message': 'Import projects from Asana is successful.' if success is True else 'Import projects from Asana is not successful.',
            'sticky': True,
            'type': 'success' if success is True else 'danger'
        }
    }
    return notification


def action_import_project_stages(project_gid, api_client):
    """
    Method action_import_project_stages used to import the project stages from
    asana to odoo
    """
    api_instance = asana.SectionsApi(api_client)
    section_response = api_instance.get_sections_for_project(
        project_gid)
    return section_response


class ResConfigSettings(models.TransientModel):
    """
    Inherits the model Res Config Settings to add extra fields and
    functionalities to this model
    """
    _inherit = 'res.config.settings'

    workspace_gid = fields.Char(string='Workspace ID',
                                help='ID of the workspace in asana',
                                config_parameter='asana_odoo_connector.workspace_gid')
    app_token = fields.Char(string='App Token',
                            help='Personal Access Token of the corresponding '
                                 'asana account',
                            config_parameter='asana_odoo_connector.app_token')

    def action_test_asana(self):
        """
        Method action_test_asana to test the connection from odoo to asana
        """
        workspace_gid = self.workspace_gid
        api_endpoint = f'https://app.asana.com/api/1.0/workspaces/{workspace_gid}'
        access_token = self.app_token
        headers = {
            'Authorization': f'Bearer {access_token}',
        }
        response = requests.get(api_endpoint, headers=headers, timeout=10)
        if response.status_code == 200:
            success = True
            notification = action_notify(success)
            self.env['ir.config_parameter'].sudo().set_param(
                'asana_odoo_connector.connection_successful', True)
            return notification
        success = False
        notification = action_notify(success)
        return notification

    
    def button_import_projects(self):
        """
        Method button_import_projects to import the project from asana to odoo
        """
        configuration = asana.Configuration()
        configuration.access_token = self.app_token
        api_client = asana.ApiClient(configuration)
        project_instance = asana.ProjectsApi(api_client)
        section_instance = asana.SectionsApi(api_client)
        workspace = self.workspace_gid
        opts = {
            'workspace': workspace
        }
        
        project_create_list = []
        project_write_list = []
        
        try:
            project_response = project_instance.get_projects(opts)
            for project in project_response:
                asana_gid = project['gid']
                project_data = project_instance.get_project(asana_gid, {})
                        
                opts = {
                    'opt_fields': "gid,name",
                }
                section_data = section_instance.get_sections_for_project(asana_gid, opts)
                type_ids = [
                    (0, 0, {'name': section['name'],
                            'asana_gid': section['gid']})
                    for section in section_data]
                
                # Import custom fields
                # CUSTOM_FIELD_TYPES = {
                #     'enum': 'tags',
                #     'multi_enum': 'tags',
                #     'text': 'text',
                #     'number': 'integer',
                #     'date': 'date',
                #     'people': 'many2many',
                # }
                # custom_fields = []
                # for field in project_response['custom_field_settings']:
                #     field_type = CUSTOM_FIELD_TYPES.get(field['custom_field']['type'])
                #     custom_fields.append({
                #         'name': field['custom_field']['gid'],
                #         'type': field_type,
                #         'string': field['custom_field']['name'],
                #         'tags': [[option['gid'], option['name'], random.randint(1, 11)] for option in field['custom_field']['enum_options']] if field_type == 'tags' else None,
                #         'selection': [[option['gid'], option['name']] for option in field['custom_field']['enum_options']] if field_type == 'selection' else None,
                #         'comodel': 'hr.employee' if field_type == 'many2many' else None,
                #         'view_in_cards': True,
                #     })
                
                project_record = self.env['project.project'].search([('asana_gid', '=', asana_gid)])
                if not project_record:
                    project_create_list.append({
                        'name': project['name'],
                        'asana_gid': asana_gid,
                        'type_ids': type_ids,
                        'description': project_data['html_notes'],
                        'user_id': False,
                        # 'task_properties_definition': custom_fields
                    })
                else:
                    project_write_list.append({
                        'name': project['name'],
                        'type_ids': type_ids,
                        'description': project_data['html_notes'],
                        # 'task_properties_definition': custom_fields
                    })
                    
            # Create projects
            self.env['project.project'].create(project_create_list)
            # Write projects
            for project in project_write_list:
                self.env['project.project'].write(project)
        except Exception as exc:
            raise ValidationError(exc)
        else:
            return action_notify_import(True)
            
    
    def button_import_tasks(self):
        """
        Method button_import_tasks to import the tasks from asana to odoo
        """
        configuration = asana.Configuration()
        configuration.access_token = self.app_token
        api_client = asana.ApiClient(configuration)
        project_instance = asana.ProjectsApi(api_client)
        workspace = self.workspace_gid
        opts = {
            'workspace': workspace
        }
        
        try:
            projects = self.env['project.project'].search([])
            for project in projects.filtered(lambda x: x.asana_gid):
                project.action_import_tasks(
                    api_client=api_client,
                )
                
            # project_response = project_instance.get_projects(opts)
            # for project in project_response:
            #     asana_gid = project['gid']
                
            #     existing_project = self.env['project.project'].search([('asana_gid', '=', asana_gid)])
            #     if existing_project:
            #         self.action_import_tasks(
            #             api_client=api_client,
            #             project_id=existing_project.id,
            #             asana_gid=asana_gid)
                    
        except Exception as exc:
            raise ValidationError(exc)
    
    def button_import_stories(self):
        """
        Method button_import_stories to import the stories from asana to odoo
        """
        configuration = asana.Configuration()
        configuration.access_token = self.app_token
        api_client = asana.ApiClient(configuration)
        story_instance = asana.StoriesApi(api_client)
        
        tasks = self.env['project.task'].search([])
        for task in tasks:
            if task.asana_gid:
            # if task.asana_gid == '1209749676226507':
                try:
                    stories_response = story_instance.get_stories_for_task(task.asana_gid, {})
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
                            user = self.env['res.users'].search([('name', '=', story['created_by']['name'])])
                        
                        # Create a comment in Odoo
                        self.env['mail.message'].create({
                            'model': 'project.task',
                            # 'body': story['text'],
                            'body': story_response['html_text'],
                            'author_id': user.id if user else False,
                            'message_type': 'comment',
                            'res_id': task.id,
                            'date': date_str,
                        })
                except Exception as exc:
                    raise ValidationError(exc)
    
    def button_delete_projects(self):
        """
        Method button_delete_projects to delete the projects in odoo
        """
        # Delete the project
        projects = self.env['project.project'].search([])
        for project in projects:
            if project.asana_gid:
                project.unlink()
    
    def button_delete_tasks(self):
        """
        Method button_delete_tasks to delete the tasks in odoo
        """
        # Delete the tasks
        tasks = self.env['project.task'].search([])
        for task in tasks:
            if task.asana_gid:
                task.sudo().unlink()
        
        
        
    def action_import_projects(self):
        """
        Method action_import_projects to import the project from asana to odoo
        """
        configuration = asana.Configuration()
        configuration.access_token = self.app_token
        api_client = asana.ApiClient(configuration)
        project_instance = asana.ProjectsApi(api_client)
        section_instance = asana.SectionsApi(api_client)
        workspace = self.workspace_gid
        opts = {
            'workspace': workspace
        }
        
        try:
            project_response = project_instance.get_projects(opts)
            for project in project_response:
                asana_gid = project['gid']
                
                # Testing with a specific project gid
                # Editorial Calendar Cyberspace
                # MVP 2.0 Requirement Gathering for HA
                # if project['gid'] not in ['1209749676226504', '1209452700341658']:
                # End testing
                    
                existing_project = self.env['project.project'].search(
                    [('asana_gid', '=', asana_gid)])
                if not existing_project:
                    project_data = project_instance.get_project(asana_gid, {})
                    
                    # opts = {}
                    opts = {
                        'opt_fields': "gid,name",
                    }
                    section_data = section_instance.get_sections_for_project(
                        asana_gid, opts)
                    type_ids = [
                        (0, 0, {'name': section['name'],
                                'asana_gid': section['gid']})
                        for section in section_data]
                    new_project = self.env['project.project'].create({
                        'name': project['name'],
                        'asana_gid': asana_gid,
                        'type_ids': type_ids,
                        'description': project_data['notes'],
                        'user_id': False,
                    })
                    self.action_import_tasks(
                        api_client=api_client,
                        project_id=new_project.id,
                        asana_gid= asana_gid)
                else:
                    self.action_import_tasks(
                        api_client=api_client,
                        project_id=existing_project.id,
                        asana_gid=asana_gid)
                    
        except Exception as exc:
            raise ValidationError(exc)
            # raise ValidationError(
            #     _('Please check the workspace ID or the app token')) from exc

    def action_import_tasks(self, api_client, project_id, asana_gid):
        """
        Method action_import_tasks to import tasks from the asana to odoo
        """
        api_instance = asana.TasksApi(api_client)
        section_instance = asana.SectionsApi(api_client)
        opts = {}
        section_data = section_instance.get_sections_for_project(asana_gid,
                                                                 opts)
        for section in section_data:
            # opts = {
            #     'opt_fields': "actual_time_minutes,approval_status,assignee,assignee.name,assignee_section,assignee_section.name,assignee_status,completed,completed_at,completed_by,completed_by.name,created_at,created_by,custom_fields,custom_fields.asana_created_field,custom_fields.created_by,custom_fields.created_by.name,custom_fields.currency_code,custom_fields.custom_label,custom_fields.custom_label_position,custom_fields.date_value,custom_fields.date_value.date,custom_fields.date_value.date_time,custom_fields.default_access_level,custom_fields.description,custom_fields.display_value,custom_fields.enabled,custom_fields.enum_options,custom_fields.enum_options.color,custom_fields.enum_options.enabled,custom_fields.enum_options.name,custom_fields.enum_value,custom_fields.enum_value.color,custom_fields.enum_value.enabled,custom_fields.enum_value.name,custom_fields.format,custom_fields.has_notifications_enabled,custom_fields.id_prefix,custom_fields.is_formula_field,custom_fields.is_global_to_workspace,custom_fields.is_value_read_only,custom_fields.multi_enum_values,custom_fields.multi_enum_values.color,custom_fields.multi_enum_values.enabled,custom_fields.multi_enum_values.name,custom_fields.name,custom_fields.number_value,custom_fields.people_value,custom_fields.people_value.name,custom_fields.precision,custom_fields.privacy_setting,custom_fields.representation_type,custom_fields.resource_subtype,custom_fields.text_value,custom_fields.type,custom_type,custom_type.name,custom_type_status_option,custom_type_status_option.name,dependencies,dependents,due_at,due_on,external,external.data,followers,followers.name,hearted,hearts,hearts.user,hearts.user.name,html_notes,is_rendered_as_separator,liked,likes,likes.user,likes.user.name,memberships,memberships.project,memberships.project.name,memberships.section,memberships.section.name,modified_at,name,notes,num_hearts,num_likes,num_subtasks,offset,parent,parent.created_by,parent.name,parent.resource_subtype,path,permalink_url,projects,projects.name,resource_subtype,start_at,start_on,tags,tags.name,uri,workspace,workspace.name", # list[str] | This endpoint returns a resource which excludes some properties by default. To include those optional properties, set this query parameter to a comma-separated list of the properties you wish to include.
            # }
            opts = {
                'opt_fields': "gid,name,assignee,assignee.name,completed,html_notes,due_on,",
            }
            task_response = api_instance.get_tasks_for_section(section['gid'], opts)
            for task in task_response:
                existing_task = self.env['project.task'].search(
                    [('asana_gid', '=', task['gid']),
                     ('project_id', '=', project_id)])
                if not existing_task:
                    task_assignee = False
                    if task['assignee']:
                        task_assignee = self.env['res.users'].search([
                            ('name', '=', task['assignee']['name']) 
                        ])
                    
                    # Create the task without child_ids
                    task_created = self.env['project.task'].create({
                        'name': task['name'],
                        'project_id': project_id,
                        'asana_gid': task['gid'],
                        'description': task['html_notes'],
                        'date_deadline': task['due_on'],
                        'state': '1_done' if task['completed'] is True else '01_in_progress',
                        # 'color': 
                        'user_ids': [(6, 0, [task_assignee.id])] if task_assignee else False,
                        'stage_id': self.env['project.task.type'].search(
                            [('asana_gid', '=', section['gid']),
                             ('project_ids', '=', project_id)]).id,
                    })
                    
                    # Create the subtask
                    subtask_response = api_instance.get_subtasks_for_task(task['gid'], opts)
                    subtask_created_list = []
                    for subtask in subtask_response:
                        existing_subtask = self.env['project.task'].search(
                            [('asana_gid', '=', subtask['gid']),
                            ('project_id', '=', project_id)])
                        if not existing_subtask:
                            subtask_assignee = False
                            if subtask['assignee']:
                                subtask_assignee = self.env['res.users'].search([
                                    ('name', '=', subtask['assignee']['name']) 
                                ])
                            
                            subtask_created = self.env['project.task'].create({
                                'name': subtask['name'],
                                'parent_id': task_created.id,
                                'asana_gid': subtask['gid'],
                                'description': subtask['html_notes'],
                                'date_deadline': subtask['due_on'],
                                'state': '1_done' if subtask['completed'] is True else '01_in_progress',
                                # 'color': 
                                'user_ids': [(6, 0, [subtask_assignee.id])] if subtask_assignee else False,
                            })
                            subtask_created_list.append(subtask_created.id)
                    
                    # Connect the subtask to the parent task using child_ids
                    task_created.write({
                        'child_ids': [(6, 0, subtask_created_list)] if len(subtask_created_list) > 0 else False,
                    })