# -*- coding: utf-8 -*-

from odoo import models, fields


class Employee(models.Model):
    _inherit = "hr.employee"

    staff_state = fields.Selection([
        (u'入职中', '入职中'),
        (u'实习期', '实习期'),
        (u'试用期', '试用期'),
        (u'正式员工', '正式员工'),
        (u'已离职', '已离职'),
    ], string="在职状态")
    staff_education = fields.Selection([
        (u'初中', '初中'),
        (u'高中/职高/中专', '高中/职高/中专'),
        (u'大学专科', '大学专科'),
        (u'大学本科', '大学本科'),
        (u'硕士', '硕士'),
        (u'博士', '博士'),
        (u'其他', '其他'),
    ], string="学历")

    leave_date = fields.Date(string="离职日期")


class Department(models.Model):
    _inherit = "hr.department"

    is_add_index = fields.Boolean('添加到首页', default=True, help="使这部门的数据可以被统计，并放到首页的统计表中")
    is_census_subordinate = fields.Boolean('统计下一级部门', default=False, help="统计部门人数时，算上下级部门")