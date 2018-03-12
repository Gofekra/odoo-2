# -*- coding: utf-8 -*-
{
    'name': "website_sale_express",

    'summary': """
            商城物流
        """,

    'description': """
        用于用户在商城查看物流信息.
        
    """,

    'author': "Gavin Gu",
    'website': "http://www.bankcall.net",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'website_sale',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'website_sale', 'website_sale_delivery', 'stock_logistics', 'website_payment_return',
                'website_sale_return'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/sale_express_templates.xml',
        'views/sale_order_templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
