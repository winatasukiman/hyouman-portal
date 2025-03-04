# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Hyouman Web Custom',
    'category': '',
    'sequence': 54,
    'summary': 'Hyouman Web Custom',
    'version': '1.0',
    'description': """""",
    'depends': [
        'web',
    ],
    'data': [
        'views/webclient_templates_custom.xml',
    ],
    'assets': {
        'web._assets_primary_variables': [
            ('prepend', 'web_custom/static/src/scss/primary_variables.scss'),
        ],
    },
    'installable': True,
    'auto_install': False,
    'application': True,
    'license': 'LGPL-3',
}
