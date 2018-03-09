# -*- coding: utf-8 -*-
###created by:chianggq@163.com 2017-02-07 10:42:51###
{
    'name': "用友项目实施管理",
    'summary': """公司内部用友项目等实施管理 """,
    'description': """
本应用主要对用友项目实施过程进行管理.
=============================================


主要内容:
----------------
* 项目计划及任务的分配
* 项目成本监控
* 项目进度跟踪
* 项目流程及文档跟踪
* 项目统计功能
    """,

    'author': "chianggq@cotong.com",
    'website': "http://www.cotong.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','account','project','hr_timesheet','hr_expense','hr_recruitment','ct_hr_payroll'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'security/access_rules.xml',
        'data/sequences.xml',
        'data/sequences.xml',
        'data/initdata.xml',
        'data/expensetype.xml',
        #'report/uf_handover_rpt.xml',
        #'report/uf_handover_tpl.xml',
        #'report/uf_handover_service_rpt.xml',
        #'report/uf_handover_service_tpl.xml',
        #'report/uf_soft_rpt.xml',
        #'report/uf_soft_tpl.xml',
        #'report/uf_soft_module_rpt.xml',
        #'report/uf_soft_module_tpl.xml',
        #'report/uf_log_rpt.xml',
        #'report/uf_log_tpl.xml',
        'report/uf_log_print_rpt.xml',
        'report/uf_log_print_tpl.xml',
        #'report/uf_log_line_rpt.xml',
        #'report/uf_log_line_tpl.xml',
        #'report/uf_rpt_milestone_rpt.xml',
        #'report/uf_rpt_milestone_tpl.xml',
        #'report/uf_rpt_stage_rpt.xml',
        #'report/uf_rpt_stage_tpl.xml',
        #'report/uf_data_static_rpt.xml',
        #'report/uf_data_static_tpl.xml',
        #'report/uf_data_dynamic_rpt.xml',
        #'report/uf_data_dynamic_tpl.xml',
        #'report/uf_work_tpl_rpt.xml',
        #'report/uf_work_tpl_tpl.xml',
        #'report/uf_work_line_rpt.xml',
        #'report/uf_work_line_tpl.xml',
        #'report/uf_work_hour_rpt.xml',
        #'report/uf_work_hour_tpl.xml',
        #'report/uf_work_wizard_rpt.xml',
        #'report/uf_work_wizard_tpl.xml',
        
        #'views/views.xml',
        'views/uf_log_view.xml',
        'views/templates.xml',
        'views/uf_handover_view.xml',
        'views/uf_handover_service_view.xml',
        'views/uf_soft_view.xml',
        'views/uf_soft_module_view.xml',
        'views/uf_log_print_view.xml',
        'views/uf_log_line_view.xml',
        'views/uf_rpt_milestone_view.xml',
        'views/uf_rpt_stage_view.xml',
        'views/uf_data_static_view.xml',
        'views/uf_data_dynamic_view.xml',
        'views/uf_work_tpl_view.xml',
        'views/uf_work_line_view.xml',
        'views/uf_work_hour_view.xml',
        'views/uf_work_wizard_view.xml',
        'views/inherit_project.xml',
        'views/inherit_users.xml',
        'wizard/uf_work_wizard_view.xml',
        'wizard/uf_logprint_wizard_view.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}