# -*- coding: utf-8 -*-
{
    'name': 'Cotong Feedback Answer',
    'version': '1.0',
    'category': 'Other',
    'summary': '问题反馈解答',
    'description': """
        模块功能：
            根据客户数据库反馈的问题进行解答推送
        """,
    'author': 'Shanghai Cotong Software Co., Ltd.',
    'website': 'http://www.qitongyun.cn',
    'depends': ['base','project_issue','ct_feedback','project_issue_stage'],
    'data': [

        'views/views.xml',

     ],
    'qweb': [

    ],
    'installable': True,
    'active': False,
    'application': False,
}
