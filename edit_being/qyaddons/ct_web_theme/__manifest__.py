# -*- coding: utf-8 -*-

{
    'name': '企通云后台主题',
    'version': '1.0',
    'category': 'web',
    'summary': '企通云主题模块',
    'description': """
        1.修改默认主题模块
        2.修改后台入口首页
        3.待办事项数据显示
        4.例行工作数据显示
        5.工作日历数据显示
        6.后台主题风格控制
        7.例行工作区块注释
    """,
    'author': 'Shanghai Cotong Software Co., Ltd.',
    'website': 'http://www.qitongyun.cn',
    'depends': [
        'web',
        'mail',
        # 'project',
        'ct_dashboard',
        # 'ct_routine_task'
    ],
    'data': [
        'views/webclient_templates.xml',
        'views/switch/config.xml',
        'views/switch/model.xml'
    ],
    'qweb': [
        "static/src/xml/*.xml",
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
