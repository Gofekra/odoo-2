# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
import datetime



class Website_base_Controller(http.Controller):

	@http.route('/website/get_user_info', type='json', auth="public")
	def get_user_info(self,**kwargs):
		"""获取用户"""
		return {'id':request.env.uid}


	@http.route('/website/create_user_info', type='json', auth="public")
	def create_user_info(self, **kwargs):
		"""获取用户"""
		event_id = kwargs['id']
		user=kwargs['uid']
		type= kwargs['jtss']
		ip= kwargs['ip']
		valus={
			'name':event_id,
			'user_id':user,
			'type':type,
			'ip':ip,
			'date':datetime.datetime.now()
		}
		request.env['back.user'].sudo().create(valus)
