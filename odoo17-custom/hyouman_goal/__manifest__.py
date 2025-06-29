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
        'web', 
        'mail',
        'project',
        'hyouman_project',
    ],
    'data': [
        # Security
        'security/goal_security.xml',
        'security/ir.model.access.csv',
        
        # Data
        'data/goal_progress_source_data.xml',
        
        # Views
        'views/goal_goal_views.xml',
        'views/goal_graph_views.xml',
        'views/menus.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'hyouman_goal/static/src/js/goal_graph.js',
            # 'https://unpkg.com/vis-network@9.1.2/styles/vis-network.min.css',
            # 'https://unpkg.com/vis-network@9.1.2/standalone/umd/vis-network.min.js',
            'https://d3js.org/d3.v7.min.js',
            'hyouman_goal/static/src/xml/goal_graph_template.xml',
        ],
    },

    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}