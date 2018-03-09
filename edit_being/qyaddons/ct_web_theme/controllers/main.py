# -*- coding: utf-8 -*-
import time
import datetime
import re
from odoo import http
from odoo.http import request
from odoo import fields, models, _


def month_get(d):
    """
    参数：datetime.date
    返回上个月第一个天和最后一天的日期时间
    :return
    date_from: 2016-01-01
    date_to: 2016-01-31
    """
    dayto = d - datetime.timedelta(days=d.day)
    date_from = datetime.date(dayto.year, dayto.month, 1)
    date_to = datetime.date(dayto.year, dayto.month, dayto.day)
    return date_from, date_to


class MailController(http.Controller):
    

    @http.route('/mail/redirect_to_messaging', type='json', auth="user")
    def get_redirect_to_messaging(self):
		"""待办事项"""
		mail_warns = []
		# print "oooooooooooooooooooooooo"
		mail_message = request.env['project.task']
		starred_partner_ids = mail_message.sudo().search([('id', '>', 0)])

		if starred_partner_ids:
			for x in starred_partner_ids:
				mail_warns.append({
                    '用户':'用户：'+x.user_id.name if x.user_id else '',
                    '阶段':x.stage_id.name if x.stage_id else '',
					'主题': '任务：'+x.name,
					'日期': x.date_assign,
					# '备注': '项目：'+re.compile(r'<[^>]+>').sub('',x.project_id.name),
                    '备注': '项目：'+x.project_id.name if x.project_id.name else '',
					'id': x.id,
					'model_name': 'project.task',
				})
    

		return mail_warns


# class NoteController(http.Controller):
    

#     @http.route('/note/redirect_to_note', type='json', auth="user")
#     def get_redirect_to_note(self):
#         """例行工作"""
#         note_tag_warns = {}
#         res_info=[]
#         note_stage = http.request.env['ct_routine_task.task_stage']
#         stage_id = note_stage.sudo().search([])
#         if stage_id:
#             for stage in stage_id:
#                 print stage.name
#                 note_tag_warns[stage.name]=[]
#                 res_info.append(stage.name)
#                 note_note = http.request.env['ct_routine_task.task']
#                 memo = note_note.sudo().search([('stage_id', '=', stage.id)])
#                 for res in memo:
#                     list={
#                         '标签': res.tag_ids.name,
#                         '主题': re.compile(r'<[^>]+>').sub('', res.name),
#                         'id': res.id,
#                         'model_name': 'ct_routine_task.task',
#                     }
#                     print list
#                     note_tag_warns[stage.name].append(list)
#         return {"name":res_info,"json":note_tag_warns}
