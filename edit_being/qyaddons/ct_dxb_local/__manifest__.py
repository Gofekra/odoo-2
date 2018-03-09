# -*- coding: utf-8 -*-

{
    'name': '店小宝POS本地化',
    'version': '1.0',
    'category': 'POS',
    'summary': '零售本地化',
    'description': """
    零售本地化：

1、修改POS界面左上角 logo

2、修改POS界面 title
    """,
    'author': 'Shanghai Cotong Software Co., Ltd.',
    'website': 'http://www.qitongyun.cn',
    'depends': [
        'point_of_sale'
    ],
    'data': [
         'views/views.xml',
         'views/pos_config_view.xml',
    ],
    'qweb': [
        'static/src/xml/pos_debranding.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': True,
}
