# -*- coding: utf-8 -*-
{
    'name': "清除业务数据",

    'summary':
        """
            清除数据
        """,

    'description':
        """
            自定义清除业务数据     
       """,

    'author': 'Shanghai Cotong Software Co., Ltd.',
    'website': "http://www.qitongyun.cn",

    'category': 'Tools',
    'version': '0.1',

    'depends': ['base'],

    # always loaded
    'data': [
        'views/views.xml',
        'security/ir.model.access.csv'
    ],

}