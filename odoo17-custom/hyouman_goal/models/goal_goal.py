from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class GoalGoal(models.Model):
    _name = 'goal.goal'
    _description = 'Goal'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    active = fields.Boolean(default=True, tracking=True)
    sequence = fields.Integer(string='Sequence', default=10, tracking=True)
    name = fields.Char(string='Goal Name', required=True, tracking=True)
    description = fields.Html(string='Description')
    
    # Related Goals
    parent_goal_ids = fields.Many2many(
        'goal.goal', 
        'goal_goal_parent_rel', 
        'child_goal_id', 
        'parent_goal_id', 
        string='Parent Goals'
    )
    sub_goal_ids = fields.Many2many(
        'goal.goal', 
        'goal_goal_parent_rel', 
        'parent_goal_id', 
        'child_goal_id', 
        string='Sub-Goals'
    )

    # Progress and Status
    progress_source = fields.Selection([ # Deprecated
        ('manual', 'Manual'),
        ('subgoals', 'From Sub-Goals'),
        ('projects', 'From Related Projects'),
        ('sections', 'From Related Sections'),
        ('tasks', 'From Related Tasks'),
    ], string='Progress Source', default='tasks', required=True, tracking=True)
    
    progress_source_ids = fields.Many2many(
        'goal.progress.source',
        string='Progress Source', tracking=True
    )
    is_progress_source_manual = fields.Boolean()

    completion_percentage = fields.Float(
        string='Completion',
        compute='_compute_completion_percentage',
        store=True,
        readonly=False,
        tracking=True,
        recursive=True
    )
    
    status = fields.Selection([
        ('on_track', 'On Track'),
        ('at_risk', 'At Risk'),
        ('off_track', 'Off Track'),
        ('achieved', 'Achieved'),
        ('partial', 'Partial'),
        ('missed', 'Missed'),
        ('dropped', 'Dropped'),
    ], string='Status', default='on_track', required=True, tracking=True)

    # Timeframe
    date_from = fields.Date(string='Date From', tracking=True)
    date_to = fields.Date(string='Date To', tracking=True)
    due_date = fields.Date(string='Due Date', tracking=True)
    period_id = fields.Many2one('goal.period')
    
    # Ownership
    goal_owner_id = fields.Many2one('res.users', string='Goal Owner', tracking=True)
    accountable_team = fields.Char(string='Accountable Team', required=True, tracking=True)
    
    # Structure & Relations
    related_project_ids = fields.Many2many(
        'project.project', 
        string='Related Projects'
    )
    related_task_ids = fields.Many2many(
        'project.task', 
        string='Related Tasks'
    )
    related_section_ids = fields.Many2many(
        'project.task.type', 
        string='Related Sections'
    )
    
    
    @api.constrains('parent_goal_ids')
    def _check_goal_hierarchy(self):
        if not self._check_m2m_recursion('parent_goal_ids'):
            raise ValidationError(_('Error! You cannot create a recursive hierarchy of goals.'))
    
    
    @api.depends('sub_goal_ids', 'sub_goal_ids.completion_percentage', 
                 'related_project_ids', 'related_project_ids.tasks.state',
                 'related_section_ids',
                 'related_task_ids', 'related_task_ids.state')
    def _compute_completion_percentage(self):
        for goal in self:
            total = count = 0.0
            for source in goal.progress_source_ids:
                # Do not recompute if source is manual, keep user's value
                code = source.code
                if code == 'manual':
                    continue
                
                if code == 'subgoals' and goal.sub_goal_ids:
                    count += sum(goal.sub_goal_ids.mapped('completion_percentage'))
                    total += len(goal.sub_goal_ids)
                
                elif code == 'projects' and goal.related_project_ids:
                    # Not using this because the closed_task_count and task_count is not stored so can't be used for filtering
                    # completed_task_total = sum(goal.related_project_ids.mapped('closed_task_count'))
                    # all_task_total = sum(goal.related_project_ids.mapped('task_count'))
                    
                    # Instead we use this
                    all_tasks = goal.related_project_ids.tasks.filtered(lambda t: not t.parent_id)
                    completed_task_total = len(all_tasks.filtered(lambda t: t.state in ['1_done']))
                    
                    all_task_total = len(all_tasks)
                    total += all_task_total
                    count += completed_task_total * 100
                    
                elif code == 'tasks' and goal.related_task_ids:
                    done_tasks = goal.related_task_ids.filtered(lambda t: t.state in ['1_done'])
                    count += len(done_tasks) * 100
                    total += len(goal.related_task_ids)
                    
                elif code == 'sections' and goal.related_section_ids:
                    all_done_tasks = all_total_tasks = 0
                    
                    sections = goal.related_section_ids
                    for section in sections:
                        tasks_in_section = self.env['project.task'].search([('stage_id', '=', section._origin.id)])
                        done_tasks = tasks_in_section.filtered(lambda t: t.state in ['1_done'])
                        all_done_tasks += len(done_tasks)
                        all_total_tasks += len(tasks_in_section)
                    
                    count += all_done_tasks * 100
                    total += all_total_tasks

            if total > 0:
                goal.completion_percentage = count / total
            else:
                goal.completion_percentage = 0.0
    
    
    @api.onchange('progress_source_ids')
    def _onchange_progress_source_ids(self):
        if len(self.progress_source_ids) > 1 and 'manual' in self.progress_source_ids.mapped('code'):
            manual = self.progress_source_ids.filtered(lambda source: source.code == 'manual')
            self.progress_source_ids = manual
            self.is_progress_source_manual = True
        else:
            self.is_progress_source_manual = False
            
        self._compute_completion_percentage()