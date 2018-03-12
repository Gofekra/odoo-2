# -*- coding: utf-8 -*-
{
    'name': '批量编辑 ',
    'summary': '批量编辑',
    'category': 'Tools',

    'description': """
   * 创建全局配置功能，
   * 针对每一个主表字段可以进行配置批量修改，清空
       """,

    'version': '1.0',
    'author': 'Gavin Gu ',

    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/mass_editing_view.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
