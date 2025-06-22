# -*- coding: utf-8 -*-
#############################################################################
#
#    Victor Imannuel
#
#    Copyright (C) 2023-TODAY Victor Imannuel(<https://www.victorimannuel.com>)
#    Author: Victor Imannuel (victorimannuel.dev@gmail.com)
#
#    You can modify it under the terms of the GNU LESSER
#    GENERAL PUBLIC LICENSE (LGPL v3), Version 3.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU LESSER GENERAL PUBLIC LICENSE (LGPL v3) for more details.
#
#    You should have received a copy of the GNU LESSER GENERAL PUBLIC LICENSE
#    (LGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
#############################################################################
{
    "name": "Modern Backend Theme",
    "version": "17.0.1.0.0",
    "category": "Themes/Backend",
    "summary": "Modern backed Theme is an attractive theme for backend",
    "description": """Minimalist and elegant backend theme for Odoo Backend""",
    "author": "Victor Imannuel",
    "company": "",
    "maintainer": "Victor Imannuel",
    "website": "https://www.linkedin.com/in/victor-imannuel",
    "depends": [
        "web", 
        "mail"
    ],
    "data": [
    ],
    'assets': {
        'web.assets_backend': [
            'modern_backend_theme/static/src/layout/style/layout_style.scss',
            'modern_backend_theme/static/src/xml/control_panel.xml',
            'modern_backend_theme/static/src/xml/search_panel.xml',
            'modern_backend_theme/static/src/xml/form_status_indicator.xml',
        ],
    },
    'images': [
        # 'static/description/banner.jpg',
        # 'static/description/theme_screenshot.jpg',
    ],
    'license': 'LGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}
