{
    'name': "Fixed Torch - Show View Type Display Name",
    'summary': """
    """,
    'description': """
    """,
    'author': "Victor Imannuel",
    'category': 'Tools',
    'version': '17.01',

    'depends': [
        'web',
    ],

    'data': [
    ],
    
    'assets': {
        'web.assets_backend': [
            (
                'after',
                'web/static/src/search/control_panel/control_panel.xml',
                'ft_show_view_type_display_name/static/src/xml/control_panel.xml',
            ),
        ],
    },
}