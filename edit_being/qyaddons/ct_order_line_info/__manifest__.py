# -*- coding: utf-8 -*-

{
    'name': 'Cotong product Info',
    'version': '1.0',
    'category': 'web',
    'summary': '产品信息模块增强',
    'description': """
        产品信息显示窗口
    """,
    'author': 'Shanghai Cotong Software Co., Ltd.',
    'website': 'http://www.qitongyun.cn',
    'depends': [
        'web',
        'sale',
        'purchase',
        'ct_vokin'
    ],
    'data': [
        'views/webclient_templates.xml',
    ],
    'qweb': [
        "static/src/xml/base.xml",
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
