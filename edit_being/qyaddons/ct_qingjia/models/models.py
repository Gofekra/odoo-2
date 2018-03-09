# -*- coding: utf-8 -*-
from odoo import models, fields, api


class qingjiadan(models.Model):
    _name = 'qingjia.qingjiadan'


    WORKFLOW_STATE_SELECTION = [
        ('draft', u'草稿'),
        ('confirm', u'待审批'),
        ('complete',u'已完成')
    ]


    name = fields.Many2one('hr.employee',string="申请人")
    days = fields.Integer(string="天数")
    startdate = fields.Date(string="开始日期")
    reason = fields.Text(string="请假事由")
    state = fields.Selection(WORKFLOW_STATE_SELECTION, default='draft', string='状态',  readonly=True)
    now_sate=fields.Selection(
        [
            ('yuang', u'员工'),
            ('bumen', u'部门经理'),
            ('fuzong', u'副总经理'),
            ('zongjin', u'总经理'),
            ('renshi', u'人事经理'),
        ],default = 'yuang', string = '审批阶段', readonly = True)


    @api.multi
    def do_confirm(self):
        self.state = 'confirm'
        return True

    @api.multi
    def do_complete(self):
        self.state = 'complete'
        return True



