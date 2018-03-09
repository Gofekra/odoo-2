# -*- coding: utf-8 -*-
import werkzeug
from wechatpy import parse_message
from wechatpy.crypto import WeChatCrypto
from wechatpy.utils import check_signature
from wechatpy import parse_message, create_reply
from wechatpy.exceptions import InvalidSignatureException, InvalidAppIdException

from odoo import http
from odoo.http import request

from .handlers import auto_reply, event_reply
import logging
_logger = logging.getLogger(__name__)

def abort(code):
    return werkzeug.wrappers.Response('Unknown Error: Application stopped.', status=code,
                                      content_type='text/html;charset=utf-8')


def handle_msg(msg):
	if msg.type == 'event':
		return event_reply.event_reply(msg)
	else:
		return auto_reply.auto_reply(msg)


class WxController(http.Controller):
	"""微信公众号验证"""
	
	def __init__(self):
		param = request.env()['ir.config_parameter']
		self.wx_token = param.get_param('wx_token') or ''
		self.wx_appid = param.get_param('wx_appid') or ''
		self.wx_AppSecret = param.get_param('wx_AppSecret') or ''
		self.wx_AESKey = param.get_param('wx_AESKey') or ''
		
		from ..rpc import oa_client
		oa_client.init_oa_client(self.wx_appid, self.wx_AppSecret)


	@http.route('/wx_handler', type='http', auth="none", methods=['GET', 'POST'],csrf=False)
	def wx_authentication(self, **kwargs):

		signature = request.params.get('signature', '')
		timestamp = request.params.get('timestamp', '')
		nonce = request.params.get('nonce', '')
		echo_str = request.params.get('echostr', '')
		encrypt_type = request.params.get('encrypt_type', 'raw')

		if request.httprequest.method == 'GET':
			try:
				check_signature(self.wx_token, signature, timestamp, nonce)
			except InvalidSignatureException:
				abort(403)
			return echo_str

		# POST
		# 返回的消息
		xml = request.httprequest.data
		if encrypt_type == 'raw':
			msg = parse_message(xml)
			_logger.info('微信回复消息msg %s',msg)  # debug
			data=handle_msg(msg)
			_logger.info('回复微信消息xml %s',data)  # debug
			return handle_msg(msg)
		else:
			crypto = WeChatCrypto(self.wx_token, self.wx_AESKey, self.wx_appid)
			try:
			    decrypted_xml = crypto.decrypt_message(
			        xml,
			        signature,
			        timestamp,
			        nonce
			    )
			except (InvalidAppIdException, InvalidSignatureException):
			    # 处理异常或忽略
			    abort(403)

			msg = parse_message(decrypted_xml)
			_logger.info('微信返回消息11111 %s', decrypted_xml)  # debug

			reply_xml = handle_msg(msg)			
			return crypto.encrypt_message(reply_xml, nonce, timestamp)
