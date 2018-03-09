# -*- coding: utf-8 -*-
#########
#Gavin Gu
#Email:guwenfengvip@163.com
#QQ:365626583
{
    'name': "import_data_by_fields",

    'summary': """
        导入时可指定某些字段来查询更新""",

    'description': """
        导入时可指定某些字段来查询更新
    """,

    'author': "Gavin GU ",
    'website': "",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Toosl',
    'version': '0.1',

    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/templates.xml',
        'views/views.xml',
    ],
    'qweb': ['static/src/*.xml'],

    # any module necessary for this one to work correctly
    'depends': ['base_import'],
}
