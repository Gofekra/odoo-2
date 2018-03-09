# -*- coding: utf-8 -*-
{
    'name': "auth_allowed_ips",

    'summary': """
        用户登录ip 正则限制""",

    'description': """
        用户登录ip 正则限制
    """,

    'author': "ZhangJie",
    'website': "http://www.bankcall.net",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['auth_login_log'],

    # always loaded
    'data': [
        'res_users_views.xml',
    ],
    'installable': True,
}
