# -*- coding: utf-8 -*-
# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
# Odoo Connector
# QQ: 978979209
# Tel：18683026906
# Author：'zengfajun'
# Date：2018-1-3
# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&

{
    'name': 'Field Verify',
    'summary': 'Field Verify',
    'version': '1.0',
    'sequence': 1,
    'author': 'Mr Zeng',
    'depends': ['base'],
    'data': [
        'views/field_verify.xml',
    ],
    'qweb': [],
    'installable': True,
    'application': True,
    'auto_install': False,
    'description': u"""
特殊字段验证包:
=====================
支持
    * 手机号码验证：widget="field_phone"
    * 邮箱验证：widget="field_email"
    * 身份证验证：widget="field_ID_card"
""",
}


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
