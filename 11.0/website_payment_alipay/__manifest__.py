# -*- coding: utf-8 -*-

{
    'name': '支付宝支付',
    'author': "Gavin Gu",
    'website': "http://www.bankcall.net",
    'category': 'Accounting',
    'summary': '支付宝支付',
    'version': '1.0',
    'description': """支付宝支付 """,
    'depends': ['payment','website_payment_return'],
    'data': [
        'templates/payment_alipay_templates.xml',
        'data/payment_acquirer_data.xml',
        'views/payment_views.xml',
    ],
    "external_dependencies": {
        "python": ["Crypto"],
    },
    'installable': True,

}
