# -*- coding: utf-8 -*-
{
    'name': "物流跟踪",

    'summary': """
        物流跟踪
        """,

    'description': """
       物流跟踪
    """,

    'author': "Gavin Gu",
    'website': "http://www.bankcall.net",

    'category': 'stock',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'stock', 'delivery'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'wizard/stock_logistics_wizard_views.xml',
    ],
    # only loaded in demonstration mode
    'installable': True,
}
