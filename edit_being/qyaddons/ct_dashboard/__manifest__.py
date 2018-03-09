# -*- coding: utf-8 -*-

{
    'name': '企通仪表板模块',
    'version': '1.0',
    'category': '技术设置',
    'summary': 'dashboard模块',
    'description': """
        1.Echart图表配置
        2.后台首页主题 待办事项|例行工作|工作日历 显示权限控制
        3.清除 echart2 例行工作仪表板配置
    """,
    'author': 'Shanghai Cotong Software Co., Ltd.',
    'website': 'www.qitongyun.cn',
    'depends': [
        'base'
    ],
    'data': [
        "views/dashboard_view.xml",
        'security/ir.model.access.csv'
    ],
    'qweb': [
        "static/src/xml/*.xml",
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
