# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Dashboard(models.Model):
    _name = 'ct.dashboard'

    name = fields.Text('名称')
    code = fields.Text('代码')
    group_ids = fields.Many2many('res.groups',string='用户组')
    #echart1 = fields.Boolean('待办事项',default=True)
    #echart2 = fields.Boolean('例行工作',default=True)

    @api.model
    def get_config(self):
        """
        提供前端显示/隐藏仪表控件列表
        :return:
        """
        groups_id = self.env.user.groups_id.ids
        showData = self.search([('group_ids','=',groups_id)])
        hideData = self.search([('group_ids','!=',groups_id)])
        hide = []
        show = []
        for d in hideData:
            if(d.code):
                hide.append(d.code)

        for d in showData:
            if(d.code):
                show.append(d.code)
        pass
        return {
            'hide':hide,
            'show':show
        }
