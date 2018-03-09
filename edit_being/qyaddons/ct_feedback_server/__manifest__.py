# -*- coding: utf-8 -*-
{
    'name': 'Cotong Feedback (Server)',
    'summary': '问题反馈',
    'description': """
        模块功能：
            客户数据库向服务器数据库反馈问题
        """,
    'author': 'Shanghai Cotong Software Co.',
    'website': 'http://www.80sERP.com',

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'project', 'project_issue','ct_project_dev'],

    # always loaded
    'data': [
        'data/data.xml',
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/wizard.xml',
        'views/templates.xml',
    ],
    'installable': True,
    'active': False,
    'application': True,

}
