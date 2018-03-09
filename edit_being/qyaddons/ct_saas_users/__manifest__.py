# -*- coding: utf-8 -*-
{
    'name': "Cotong Center Manger",
    'version': '1.0',
    'category': '',
    'summary': """
        客户身份信息""",

    'description': """
         微信访问检查微信客户的信息，
         并行电小宝账户的信息
    """,

    'author': 'Shanghai Cotong Software Co., Ltd.',
    'website': 'http://www.qitongyun.cn',

    'depends': ['base'],

    'data': [
        # 'security/ir.model.access.csv',
        'views/center.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],
}
