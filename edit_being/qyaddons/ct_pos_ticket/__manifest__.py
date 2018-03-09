# -*- coding: utf-8 -*-
{
    'name': 'POS小票',
    'summary': '修改打印小票格式',
    'description': """
    修改POS内部连接小票打印机打印出来的内容格式
    """,
    'category': 'other',
    'version': '1.0',
    'author': '今晨科技|企通软件',
    'website': 'http://www.168nz.cn/',
    'depends': ['base', 'web','point_of_sale'],
    'data': [
        'views/template.xml',
    ],
    'qweb': [
        'static/src/xml/*.xml',
    ],
    'installable': True,
    'application': True,
}