# -*- coding: utf-8 -*-
{
    'name': "website_sale_return",

    'summary': """
        退货操作
        """,

    'description': """
        退货操作
    """,

    'author': "Gavin Gu",
    'website': "http://www.bankcall.net",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'website',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'website_sale_stock', 'website_sale_management'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
