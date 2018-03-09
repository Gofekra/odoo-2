# -*- coding: utf-8 -*-

{
    'name': '店小宝企通云主题',
    'version': '1.0',
    'category': 'web',
    'summary': '企通云Pos兼容主题模块',
    'description': """
        集成以前web主题部分样式
    """,
    'author': 'Shanghai Cotong Software Co., Ltd.',
    'website': 'http://www.qitongyun.cn',
    'depends': [
        'web'
    ],
    'data': [
        'views/webclient_templates.xml',
        'views/switch/config.xml',
        'views/switch/model.xml'
    ],
    'qweb': [
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
