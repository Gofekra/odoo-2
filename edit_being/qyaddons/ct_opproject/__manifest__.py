# -*- coding: utf-8 -*-
{
    'name': "opproject",

    'summary': """ """,
		

    'description': """
       项目延伸功能：实现销售与项目动作自动关联，并触发    """,

    'author': "Shanghai Cotong Software Co., Ltd.",
    'website': "http://www.yourcompany.com",


    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','sale','project','hr_timesheet','stock'],

    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/views.xml',
        # 'views/templates.xml',
        'demo/demo.xml',
    ],
    # only loaded in demonstration mode
    'demo': [

    ],
    'installable': True,
    'active': False,
    'application': False,
}