/** @odoo-module */

import { patch } from '@web/core/utils/patch';
import { ProjectTaskKanbanRenderer } from '@project/views/project_task_kanban/project_task_kanban_renderer';
import { useService } from '@web/core/utils/hooks';
import { onWillStart } from "@odoo/owl";

patch(ProjectTaskKanbanRenderer.prototype, {
    setup() {
        // Call original setup
        super.setup();
        const user = useService("user");

        onWillStart(async () => {
            // Project Manager access rights applied for project manager and project power user
            this.isProjectManager = await user.hasGroup('project.group_project_manager') || await user.hasGroup('hyouman_project_power_user.group_project_power_user');
        });
    },
});