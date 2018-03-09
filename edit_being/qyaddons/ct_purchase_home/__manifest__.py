# -*- coding: utf-8 -*-

{
    'name': 'Cotong Purchase Home',
    'version': '1.0',
    'category': 'purchase',
    'summary': '采购首页',
    'description': """
        采购首页:

1、柱状图显示采购TOP5，按金额/数量显示采购存货TOP5;

2、柱状图显示采购入库排程;
    """,
    'author': 'Shanghai Cotong Software Co., Ltd.',
    'website': 'http://www.qitongyun.cn',
    'depends': [
        'purchase',
        'ct_dashboard'
    ],
    'data': [
        "views/purchase_index_view.xml",
    ],
    'qweb': [
        "static/src/xml/*.xml",
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
