/** @odoo-module */

import { patch } from '@web/core/utils/patch';
import { useService } from '@web/core/utils/hooks';

import { NavBar } from '@web/webclient/navbar/navbar';
import { AppsMenu } from "@muk_web_theme/webclient/appsmenu/appsmenu";

patch(NavBar.prototype, {
	setup() {
        super.setup();
        this.appMenuService = useService('app_menu');
        this.sidebarHidden = false;
    },
    onToggleSidebar() {
        const sidebar = document.querySelector('.mk_apps_sidebar_panel');
        const sidebarLogo = document.querySelector('.mk_apps_sidebar_logo');
        if (sidebar) {
            this.sidebarHidden = !this.sidebarHidden;
            sidebar.classList.toggle('hide-animate', this.sidebarHidden);
            sidebarLogo.classList.toggle('hide-animate', this.sidebarHidden);
            this.render();  // Re-render to update the icon
        }
    }
});

patch(NavBar, {
    components: {
        ...NavBar.components,
        AppsMenu,
    },
});
