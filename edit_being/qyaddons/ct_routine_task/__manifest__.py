# -*- coding: utf-8 -*-
{
    'name': 'Routine Tasks',
    'version': '1.0',
    'category': 'Project',
    'summary': 'Manage routine task',
    'description': """Routine Task Management""",
    'author': 'Shanghai Cotong Software Co., Ltd.',
    'website': 'http://www.qitongyun.cn',
    'depends': [
        'base_setup',
        'resource',
        'web_kanban',
        'web_planner',
        'web_tour',
    ],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/views.xml',
        'data/data.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}

