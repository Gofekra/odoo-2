# -*- coding: utf-8 -*-
{
    'name': "website_payment_return",

    'summary': """
        在线支付之后处理退款
        """,

    'description': """
       在线支付之后处理退款
    """,

    'author': "Gavin Gu",
    'website': "http://www.bankcall.net",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'website',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'payment', 'website_sale_return'],

    # always loaded
    'data': [
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
