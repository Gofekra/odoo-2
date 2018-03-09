# -*- coding: utf-8 -*-
{
    'name': "qingjia",

    'summary': """
        请假模块""",

    'description': """
        请假模块
    """,

    'author': "Ltd",
    'website': "http://www.qitongyun.cn",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': '',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','hr'],

    # always loaded
    'data': [
        'security/group_view.xml',
        #'security/ir.model.access.csv',
        'views/views.xml',
        'views/workflow.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}