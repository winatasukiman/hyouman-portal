{
    'name': "Hyouman - Project",
    'summary': """
        Hyouman custom project module for Odoo 17
    """,
    'description': """
        Hyouman custom project module for Odoo 17
    """,
    'author': "Victor Imannuel",
    'category': 'Project',
    'version': '17.01',

    'depends': [
        'project',
    ],

    'data': [
        # Views
        'views/project_views.xml',
        'views/project_task_views.xml',
        'views/project_task_type_views.xml',
        'views/menu_views.xml',
    ],
}