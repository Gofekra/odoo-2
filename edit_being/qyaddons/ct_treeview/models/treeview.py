# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Treeview(models.Model):
    _name = 'ct.treeview'
    """创建位置存取表"""
    name = fields.Text('名称')
    code = fields.Text('代码')
    group_ids = fields.Many2one('res.partner',string='用户组')
