# -*- coding: utf-8 -*-
{
    'name': "跨域注册、微信绑定",

    'summary': """
        跨域注册、微信绑定
        """,

    'description': """
       跨域注册、微信绑定
    """,

    'author': 'Shanghai Cotong Software Co., Ltd.',
    'website': 'http://www.qitongyun.cn',

    'category': 'web',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','ct_wechat'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}