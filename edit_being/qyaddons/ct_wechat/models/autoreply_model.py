# -*- coding: utf-8 -*-
from odoo import models, fields, api


# 在这添加可发送的内容，如音频，视频等
REPLY_CONTENT = [
		('wx.image', '图片'), 
		('wx.text', '文字'),
		('wx.imagetext', '单图文'),
		('wx.many.imagetext', '多图文'),
	]


class FollowAutoReply(models.Model):
	_name = 'wx.follow.autoreply'
	_inherit = 'res.config.settings'

	content = fields.Reference(string='内容', selection=REPLY_CONTENT)


class MessageAutoReply(models.Model):
	_name = 'wx.message.autoreply'
	_inherit = 'res.config.settings'

	content = fields.Reference(string='内容', selection=REPLY_CONTENT)


class KeywordAutoReply(models.Model):
	_name = 'wx.keyword.autoreply'

	name = fields.Char('规则名')
	keyword = fields.Char('关键字')
	content = fields.Reference(string='内容', selection=REPLY_CONTENT)
	matched_type = fields.Selection([(1,'完全匹配'),(2,'模糊匹配')], '匹配方式', default=1, 
		help="选择'完全匹配'，只有当用户发送的信息和关键字完全一样时才回复此文本。而'模糊匹配'则只要用户发送信息中有此关键字就行。")