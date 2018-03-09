# -*- coding: utf-8 -*-
from wechatpy.replies import TextReply
from wechatpy.replies import ImageReply
from wechatpy.replies import ArticlesReply
from odoo.http import request
import odoo
import logging
_logger = logging.getLogger(__name__)


def handle_reply(content, msg):
	'''
	根据用户选取的回复信息的类型，对相应信息进行处理成xml
	'''
	env = request.env()
	if content._name == 'wx.text':
		reply_content = content.text_content
		reply =TextReply(message=msg, content=reply_content)
	elif content._name == 'wx.image':
		reply_content = content.media_id
		reply = ImageReply(media_id=reply_content, message=msg)
	elif content._name == 'wx.imagetext':
		Articles = [
			{
				'title':content.name,
				'description':content.content,
				'picurl':content.image_id.url,
				'url':content.content_source_url
			 }
		]
		reply =  ArticlesReply(
            message=msg,
            articles=Articles
        )
	elif content._name == 'wx.many.imagetext':
		Articles=[]
		for content in content.many_image_text:
			Articles.append(
				{
					'title': content.name,
					'description': content.content,
					'picurl': content.image_id.url,
					'url': content.content_source_url
				}

			)
		reply = ArticlesReply(
			message=msg,
			articles=Articles
		)

	_logger.info('消息处理reply %s', reply)  # debug
	return reply.render()




def auto_reply(msg):
	'''
	根据用户消息回复的设置，给非事件消息自动回复消息
	'''
	env = request.env()
	if msg.type == 'text':
		msg_content = msg.content.lower()
		keywords = env['wx.keyword.autoreply'].sudo().search([])
		# 关键字匹配
		if keywords:
			for keyword_one in keywords:
				if keyword_one.matched_type == 1:
					if keyword_one.keyword == msg_content:
						return handle_reply(keyword_one.content,msg)
				else:
					if keyword_one.keyword in msg_content:
						return handle_reply(keyword_one.content,msg)
		else:
			# 关键字不匹配后，自动回复
			return reply_default(msg)
	else:
		return reply_default(msg)


def reply_default(msg):
	'''
	回复默认值
	'''
	env = request.env()
	message_aps = env["wx.message.autoreply"].sudo().search([])
	lenght = len(message_aps)
	if lenght != 0:
		message_ap = message_aps[-1]
		return handle_reply(message_ap.content, msg)
	else:
		return create_reply('关键字不匹配！',msg)

#
# def send_mess_livechat():
#
# 	# 客服对话
# 	uuid = session.get("uuid", None)
# 	ret_msg = ''
# 	cr, uid, context, db = request.cr, request.uid or openerp.SUPERUSER_ID, request.context, request.db
# 	if not client.UUID_OPENID.has_key(db):
# 		client.UUID_OPENID[db] = {}
# 	if not uuid:
# 		Param = request.env()['ir.config_parameter']
# 		channel_id = Param.get_param('wx_channel') or 0
# 		channel_id = int(channel_id)
#
# 		info = client.wxclient.get_user_info(openid)
# 		anonymous_name = info.get('nickname', '微信网友')
#
# 		reg = openerp.modules.registry.RegistryManager.get(db)
# 		session_info = request.env["im_livechat.channel"].get_mail_channel(channel_id, anonymous_name)
# 		if session_info:
# 			uuid = session_info['uuid']
# 			session["uuid"] = uuid
# 		ret_msg = '请稍后，正在分配客服为您解答'
#
# 	if uuid:
# 		client.UUID_OPENID[db][uuid] = openid
#
# 		message_type = "message"
# 		message_content = content
# 		request_uid = request.session.uid or openerp.SUPERUSER_ID
# 		author_id = False  # message_post accept 'False' author_id, but not 'None'
# 		if request.session.uid:
# 			author_id = request.env['res.users'].sudo().browse(request.session.uid).partner_id.id
# 		mail_channel = request.env["mail.channel"].sudo(request_uid).search([('uuid', '=', uuid)], limit=1)
# 		message = mail_channel.sudo(request_uid).with_context(mail_create_nosubscribe=True).message_post(
# 			author_id=author_id, email_from=False, body=message_content, message_type='comment',
# 			subtype='mail.mt_comment', content_subtype='plaintext')
#
# 	return ret_msg