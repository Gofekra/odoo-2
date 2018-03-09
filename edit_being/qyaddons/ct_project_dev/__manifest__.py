# -*- coding: utf-8 -*-

{
    'name': 'Cotong Development Project Management',
    'version': '1.0',
    'category': 'project',
    'summary': '开发项目管理模块',
    'description': '',
    'author': 'Shanghai Cotong Software Co., Ltd.',
    'website': 'https://www.80sERP.com',
    'depends': [
        'project',
        'project_issue',
    ],
    'data': [
        "data/data.xml",
        "security/ir.model.access.csv",
        "security/security.xml",
        "views/project_task_form_view.xml",
        "views/project_issue.xml",
        "views/project_issue_stage.xml",
        "views/config_view.xml",
        "views/wizard.xml",
    ],
    'qweb': [
    ],
    'installable': True,
}
