# -*- coding: utf-8 -*-
{
    'name': "物流管理",

    'summary': """
        物流管理--快递鸟平台应用
        """,

    'description': """
       单号识别
       即时查询
       预约取件
       电子面单
       物流跟踪
    """,


    'author': "Shanghai Cotong Software Co., Ltd.",
    'website': "http://www.qitongyun.cn/",


    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','stock','delivery','ct_sales'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/message_log.xml',
    ],
    # only loaded in demonstration mode
    'installable': True,
    'active': False,
    'application': False,
}