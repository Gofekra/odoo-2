# coding:utf-8

from odoo import fields,models

class hm_users(models.Model):
		_inherit='res.users'

		city=fields.Many2one('hm.city',string='city')

