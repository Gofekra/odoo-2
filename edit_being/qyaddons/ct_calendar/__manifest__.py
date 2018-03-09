# -*- coding: utf-8 -*-
{
    'name': "Cotong Calendar",

    'summary': "日历增强模块",
    'author': 'Shanghai Cotong Software Co., Ltd.',
    'website': 'https://www.qitongyun.cn',
    'category': 'Tools',
    'version': '1.0',
    'description': """
        模块功能：
        
        1. 增加客户关联；
        
        2. 添加费用关联表格；
        
        3.将费用与日程关联，在”费用“列表显示客户、描述
    """,
    'depends': [
        'base',
        'calendar',
        'project',
        'hr_expense'
    ],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/res_config.xml',
        'views/templates.xml',
        'data/data.xml',
    ],
    'installable': True,
}
