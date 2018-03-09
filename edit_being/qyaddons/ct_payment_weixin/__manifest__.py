# -*- coding: utf-8 -*-

{
    'name': '微信支付',
    'category': 'Website',
    'summary': '微信支付',
    'version': '1.0',
    'description': """商城微信支付""",
    'author': "Shanghai Cotong Software Co., Ltd.",
    'website': "http://www.qitongyun.cn/",
    'depends': ['payment'],
    'data': [
        'views/weixin.xml',
        'views/payment_acquirer.xml',
        'data/weixin.xml',
    ],
    'installable': True,
    'active': False,
    'application': False,
}
