{
    'name': "企通云网站注册模块",
    'summary': '注册优化模块',
    'description': """
        修改注册模块:

1.修改注册模块界面

2.增加服务条款界面
    """,
    'category': 'Extra Tools',
    'version': '1.0',
    'depends': [
        'auth_signup',
        'ct_marketing_message',
        'web',
    ],
    'data': [
        'views/service_view.xml',
        'views/module_view.xml',
        'views/module_intro.xml',
    ],
    'author': 'cc',
    'website': 'https://www.qitongyun.cn',
    'installable': True,
    'bootstrap': True,
}
