# -*- coding: utf-8 -*-
{
    'name': "畅捷支付网站端",

    'summary': """
        畅捷支付_website
        
        """,

    'description': """
         1、订单号一维码
        2、畅捷推送支付结果
        3、响应请求并处理
    """,


    'author': 'Shanghai Cotong Software Co., Ltd.',
    'website': 'https://www.80sERP.com',
    'category': 'Website',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['payment'],

    # always loaded
    'data': [
        'views/payment_views.xml',
        'views/payment_alipay_templates.xml',
        'views/account_config_settings_views.xml',
        'demo/payment_acquirer_data.xml',
    ],
    # only loaded in demonstration mode
    'installable': True,
    'active': False,
    'application': False,
}