# -*- coding: utf-8 -*-

{
    'name': 'Cotong HR Home',
    'version': '1.0',
    'category': 'hr',
    'summary': '员工首页',
    'description': """
        员工首页:

1、信息栏统计试用期/实习期/总人数;

2、信息栏统计新人人数/在职人数/离职人数;

3、信息栏统计未签合同/已签合同/合同到期人数;

4、环形图按部门统计当前部门员工人数，可选择显示;

5、环形图按员工在职状态统计人数;

5、环形图按性别统计在职员工性别比例;

6、柱状图按员工年龄统计人数;

7、柱状图按学历统计人数;
    """,
    'author': 'Shanghai Cotong Software Co., Ltd.',
    'website': 'http://www.qitongyun.cn',
    'depends': [
        'hr',
        'hr_contract',
        'hr_payroll',
        'ct_dashboard'
    ],
    'data': [
        "views/hr_index_view.xml",
    ],
    'qweb': [
        "static/src/xml/*.xml",
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
