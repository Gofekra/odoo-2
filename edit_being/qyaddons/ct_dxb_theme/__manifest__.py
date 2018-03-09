# -*- coding: utf-8 -*-
{
    'name': '店小宝POS主题',
    'version': '1.0',
    'category': 'POS',
    'summary': '企通云Pos主题模块',
    'description': """
    店小宝前台核心模块:
1.修改整体页面结构
2.修改风格
3.增加首页
    """,
    'author': 'Shanghai Cotong Software Co., Ltd.',
    'website': 'http://www.qitongyun.cn',
    'depends': [
        'web',
        'ct_dxb_weixin',
        'ct_dashboard',
        'ct_dxb',
        'ct_pos_home',
        'ct_dxb_home',
        'ct_legal_page',
    ],
    'data': [
        'views/webclient_template.xml',
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

