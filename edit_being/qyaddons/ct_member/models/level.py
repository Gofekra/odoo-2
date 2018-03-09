# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.tools import html2plaintext
from odoo import tools, _
from odoo.exceptions import ValidationError
from odoo.modules.module import get_module_resource


class MemberLevel(models.Model):

    _name = "member.level"
    _order = "sequence"

    name = fields.Char(u'名称')
    code = fields.Char(u'编码')
    discount = fields.Float(u'折扣')
    sequence = fields.Integer(u'顺序', default = 1)


    _sql_constraints = [
        ('name_uniq', 'unique (name)', "Tag name already exists !"),
    ]







