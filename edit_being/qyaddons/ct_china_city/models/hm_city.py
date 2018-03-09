#coding:utf-8

from odoo import fields,models

class hm_city(models.Model):
		_name='hm.city'


		name=fields.Char(string='name')
		state=fields.Many2one('res.country.state','state')



class hm_district(models.Model):
		_name="hm.district"

		name=fields.Char(string='name')
		city=fields.Many2one('hm.city',string="city")

