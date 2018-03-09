# -*- coding: utf-8 -*-
{
    'name': '店小宝Pos报表',
    'version': '1.0',
    'category': 'POS',
    'summary': '店小宝Pos报表模块',
    'description': """
    店小宝POS后台核心模块:
1.增加POS模块报表视图
    """,
    'author': 'Shanghai Cotong Software Co., Ltd.',
    'website': 'http://www.qitongyun.cn',
    'depends': [
        'base',
        'web',
        'point_of_sale',
        'pos_loyalty',
        'contacts',
        'sale',
        'decimal_precision'
    ],
    'data': [
        'views/views.xml',
        'views/report.xml',
        'views/hidden_fields.xml',
        'data/res_config.xml',
        'views/user_config.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}

