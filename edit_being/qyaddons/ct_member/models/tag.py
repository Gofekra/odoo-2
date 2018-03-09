# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.tools import html2plaintext
from odoo import tools, _
from odoo.exceptions import ValidationError
from odoo.modules.module import get_module_resource


class MemberTag(models.Model):

    _name = "member.tag"
    _order = "sequence"

    name = fields.Char(u'标签')
    sequence = fields.Integer(u'顺序', default = 1)

    _sql_constraints = [
        ('name_uniq', 'unique (name)', "Tag name already exists !"),
    ]







