# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Hyouman Portal Time Off',
    'category': '',
    'sequence': 54,
    'summary': 'Hyouman Portal Time Off',
    'version': '1.0',
    'description': """""",
    'depends': [
		'hr_holidays'
    ],
    'data': [
        'views/hr_leave_views.xml',
    ],
    'assets': {
    },
    'installable': True,
    'auto_install': False,
    'application': True,
    'license': 'LGPL-3',
}
