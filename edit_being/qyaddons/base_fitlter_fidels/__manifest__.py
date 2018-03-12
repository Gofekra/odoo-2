# -*- coding: utf-8 -*-
{
    'name': "高级搜索扩展",

    'summary': """
        高级搜索扩展
        """,

    'description': """
       增加一个标识符字段，用于在高级搜索时，过滤出我们不想要的字段
    """,
    'author': 'Gavin Gu',
    'website': '',

    'category': 'Other',
    'version': '0.1',
    'depends': ['base','sale'],

    'data': [
        'views/views.xml',
        'views/templates.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],
    'qweb': [
        "static/src/xml/*.xml",
    ],
}