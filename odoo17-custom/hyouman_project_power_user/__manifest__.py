{
    'name': "Hyouman - Project Power User",
    'summary': "To add new access rights for project: Power User",
    'description': """
        To add new access rights for project: Power User
        - Have same record rule as project user role
        - Able to create new project and adjust the settings
    """,
    'author': "Victor Imannuel",
    'website': 'https://victor.imannuel.kartika.web.id',
    'category': 'Project',
    'version': '17.0.1.0.0',

    'depends': [
        'project',
    ],

    'data': [
        # Security
        'security/project_security.xml',
        'security/ir.model.access.csv',
        
        # Views
        'views/menus.xml',
    ],
}