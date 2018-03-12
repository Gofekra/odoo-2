# -*- coding: utf-8 -*-

{
    'name': '微信支付',
    'category': 'Website',
    'summary': '微信支付',
    'version': '11.1.0',
    'description': """商城微信支付""",
    'author': "Gavin Gu",
    'website': "http://www.bankcall.net",
    'depends': ['payment', 'website_payment_return'],
    'data': [
        'templates/payment_weixin_templates.xml',
        'data/weixin.xml',
        'views/payment_acquirer.xml',

    ],
    'installable': True,
}
