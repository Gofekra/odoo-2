# -*- coding: utf-8 -*-

{
    'name': 'Cotong Treeview',
    'version': '1.0',
    'category': 'treeview',
    'summary': 'treeview模块',
    'description': """
        treeview排序
    """,
    'author': 'Shanghai Cotong Software Co., Ltd.',
    'website': 'http://www.qitongyun.cn',
    'depends': [
        'web',
        'ct_dashboard'
    ],
    'data': [
        "views/treeview_view.xml",
        'security/tree_security.xml',
        'security/ir.model.access.csv',
        'wizard/change_tree_view_wizard_view.xml',
        'views/customize_tree.xml'
    ],
    'images': ['images/1.png', 'images/2.png', 'images/3.png', 'images/4.png', 'images/5.png', 'images/6.png'],
    'qweb': [
        "static/src/xml/*.xml",
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
