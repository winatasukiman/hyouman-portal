/** @odoo-module **/

import { _t } from "@web/core/l10n/translation";
import { patch } from '@web/core/utils/patch';
import { ProjectTaskKanbanHeader } from '@project/views/project_task_kanban/project_task_kanban_header';

patch(ProjectTaskKanbanHeader.prototype, {
    async onWillStart() {
        super.onWillStart();
        
        if (this.props.list.isGroupedByStage) { // no need to check it if not grouped by stage
            // Project Manager access rights applied for project manager and project power user
            this.isProjectManager = await this.userService.hasGroup('project.group_project_manager') || await this.userService.hasGroup('hyouman_project_power_user.group_project_power_user');
        }
    }
});