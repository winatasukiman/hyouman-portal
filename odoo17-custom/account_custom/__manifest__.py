# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Hyouman Invoicing Custom',
    'category': '',
    'sequence': 54,
    'summary': 'Hyouman Invoicing Custom',
    'version': '1.0',
    'description': """""",
    'depends': [
        'account',
    ],
    'data': [
        'data/mail_template_data.xml',
        'views/account_move_views.xml',
        'views/report_templates.xml',
    ],
    'assets': {
    },
    'installable': True,
    'auto_install': False,
    'application': True,
    'license': 'LGPL-3',
}
