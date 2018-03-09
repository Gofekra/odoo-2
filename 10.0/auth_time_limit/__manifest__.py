# -*- coding: utf-8 -*-
{
    'name': "auth_time_limit",

    'summary': """
        登录次数限制""",

    'description': """
        登录次数限制
    """,

    'author': "ZhangJie",
    'website': "http://www.bankcall.net",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'ir_config_parameter_data.xml',

        'views.xml',
    ],
    'installable': True,
}
