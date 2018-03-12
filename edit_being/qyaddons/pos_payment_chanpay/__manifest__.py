# -*- coding: utf-8 -*-
{
    'name': "畅捷支付_POS",

    'summary': """
        畅捷支付_POS    
        """,
    'description': """
         畅捷支付：支付流程：
        1、订单号一维码
        2、畅捷推送支付结果
        3、响应请求并处理
    """,

    'author': 'Gavin Gu',
    'website': '',

    'category': 'POS',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['base','point_of_sale'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
    ],
    'qweb': [
        "static/xml/*.xml",
    ],
    # only loaded in demonstration mode
    'installable': True,
    'active': False,
    'application': False,
}