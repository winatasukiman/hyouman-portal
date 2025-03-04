# -*- coding: utf-8 -*-

{
    "name": "Show/hide password login page",
    "version": "16.0.1",
    "license": "OPL-1",
    "support": "relief.4technologies@gmail.com",  
    "author": "Relief Technologies",
    "category": "Website/Website",
    "summary": "Show/hide password in login page",
    "description": """
    """,
    'depends': [
        'web',
    ],
    'data': [
        'views/login_page.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'rt_hide_show_password/static/src/scss/style.scss',
            'rt_hide_show_password/static/src/js/custom.js',
        ],
    },
    "images": ["static/description/background.png",],
    "application": True,
    "auto_install": False,
    "installable": True,
    "price": 0,
    "currency": "EUR"   
}
