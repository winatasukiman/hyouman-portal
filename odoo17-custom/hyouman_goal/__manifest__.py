{
    'name': 'Hyouman - OKR Management',
    'version': '17.0.1.0.0',
    'summary': 'Manage company, team, and individual goals (OKRs).',
    'description': """
        A comprehensive module to create, track, and manage hierarchical goals.
        Features:
        - Parent/Sub-goal relationships
        - Automated progress calculation from sub-goals, projects, or tasks
        - Configurable goal periods and sections
        - Clear ownership and accountability
    """,
    'author': 'Victor Imannuel',
    'website': 'https://www.thehyouman.com',
    'category': 'Human Resources/Productivity',
    'depends': [
        'base', 
        'mail',
        'project',
    ],
    'data': [
        'security/goal_security.xml',
        'security/ir.model.access.csv',
        # 'data/goal_data.xml',
        'views/goal_period_views.xml',
        'views/goal_section_views.xml',
        'views/goal_goal_views.xml',
        'views/menus.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}