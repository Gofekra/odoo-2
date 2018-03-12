# -*- coding: utf-8 -*-

{
    'name': 'Alipay Payment Acquirer',
    'author': "Gavin Gu",
    'website': "",
    'category': 'website',
    'summary': '支付宝支付',
    'version': '1.0',
    'description': """支付宝支付""",
    'depends': ['payment'],
    'data': [
        'views/payment_views.xml',
        'views/payment_alipay_templates.xml',
        'views/account_config_settings_views.xml',
        'data/payment_acquirer_data.xml',
    ],
    'installable': True,
    'active': True,
    'application': False,
}
