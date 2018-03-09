# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and licensing details.

{
    'name': '项目团队管理',

    'summary': '项目团队管理',
    'category': 'Project Management',
    'description': """
   * 建立项目团队

       """,
    'author': 'Shanghai Cotong Software Co., Ltd.',
    'website': "http://www.qitongyun.cn",

    'version': '1.0',
    'depends': ['project', 'crm', 'web'],
    'data': [
        'views/template.xml',
        'views/project_team_view.xml',
    ],
    'images': ['static/description/ProjectTeam.png'],
    'installable': True,
    'auto_install': False
}
