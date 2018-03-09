# -*- coding: utf-8 -*-
{
    'name': 'Cotong Feedback (Client)',
    'version': '1.0',
    'category': 'Other',
    'summary': '问题反馈',
    'description': """
        模块功能：
            客户数据库向服务器数据库反馈问题
        """,
    'author': 'Shanghai Cotong Software Co.',
    'website': 'http://www.80sERP.com',
    'depends': ['base','im_livechat'],
    'data': [
        # 'view/snippets_css_js.xml',
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'data/data.xml',
    ],
    'qweb': [
        "static/src/xml/*.xml",
    ],
    'installable': True,
    'active': False,
    'application': True,
}
