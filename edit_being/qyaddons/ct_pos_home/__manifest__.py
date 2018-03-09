# -*- coding: utf-8 -*-
{
    'name': '企通云Pos前台模块',
    'version': '1.0',
    'category': 'POS',
    'summary': 'Pos前台模块',
    'description': """
    修改Pos前台模块:

1.修改POS前台界面样式
    """,
    'author': 'Shanghai Cotong Software Co., Ltd.',
    'website': 'http://www.qitongyun.cn',
    'depends': [
        'point_of_sale',
        'ct_dxb_local',
        'ct_pos_ticket'
    ],
    'data': [
        'views/pos_index_view.xml',
        'views/pos_template.xml',
    ],
    'qweb': [
        "static/src/xml/*.xml",
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}

