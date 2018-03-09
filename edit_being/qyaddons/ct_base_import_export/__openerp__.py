# -*- coding: utf-8 -*-

{
    "name": "Cotong Data Import/Export Rules",
    'author': "Shanghai Cotong Software Co., Ltd.",
    'website': "http://www.qitongyun.cn",
    'category': 'Tools',
    'version': '1.0',
    "summary": "数据导入导出权限管理",
    "description": """
    """,
    "depends": [
        'web',
        'base_import'
    ],
    "data": [
        'security/data_impexp_security.xml',
        'views/webclient_templates.xml',
    ],
    "installable": True,
}
