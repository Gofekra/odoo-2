# -*- coding: utf-8 -*-
{
    'name': '店小宝微信网页',
    'version': '1.0',
    'category': 'POS',
    'summary': 'Pos微信网页',
    'description': """
1.将PC端部分页面制作为微信专用页面
    """,
    'author': 'Shanghai Cotong Software Co., Ltd.',
    'website': 'http://www.qitongyun.cn',
    'depends': [
        'web',
        'point_of_sale'
    ],
    'data': [
        'views/weixin_module.xml',
        'views/weixin_template.xml',
    ],
    'qweb': [
        "static/src/xml/*.xml",
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}

