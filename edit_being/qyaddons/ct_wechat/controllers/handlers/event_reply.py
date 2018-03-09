# -*- coding: utf-8 -*-
from datetime import datetime
from wechatpy import create_reply
from wechatpy.replies import ImageReply
import time
import urllib2
from odoo.http import request
import auto_reply
from ...rpc import oa_client
import urlparse
import logging
import json
from odoo import http
import httplib, urllib

_logger = logging.getLogger(__name__)

def event_reply(msg):
    """根据不同的事件回复"""
    env = request.env()
    event_type = msg.event
    if event_type == 'subscribe':
        subscribe_handler(msg)
        follow_reply = env['wx.follow.autoreply'].sudo().search([])
        if len(follow_reply) > 0:
            return auto_reply.handle_reply(follow_reply[-1].content, msg)
        else:
            return create_reply('终于等到你！', msg).render()
    elif event_type == 'unsubscribe':
        unsubscribe_handler(msg)
        return create_reply('欢迎下次关注！', msg).render()
    elif event_type == 'click':#点击菜单拉取消息时的事件推送
        pass
    elif event_type == 'view':#点击菜单跳转链接时的事件推送
         pass

def subscribe_handler(message):
    """关注事件处理，将该用户信息存入本地数据库"""
    env = request.env()
    openid = message.source
    info = oa_client.client.user.get(openid)
    info['sex'] = int(info['sex'])
    info['subscribe_time'] = stamp_to_time(info['subscribe_time'])
    rs = env['wx.user'].sudo().search([('openid', '=', openid)])
    if not rs.exists():
        info['subscribe'] = 1
        env['wx.user'].sudo().create(info)


def unsubscribe_handler(message):
    """取消关注事件，从本地数据库删除该用户数据"""
    openid = message.source
    env = request.env()
    rs = env['wx.user'].sudo().search([('openid', '=', openid)])
    if rs.exists():
        rs.unlink()

#
# def stamp_to_time(stamp, format="%Y-%m-%d %H:%M:%S"):
#     """将时间戳转换成想要的时间格式"""
#     stamp = str(stamp)
#     time_tuple = datetime.fromtimestamp(stamp)
#     return time_tuple.datetime.fromtimestamp(format)

#转化时间戳
def stamp_to_time(strtime):
    strtime = time.localtime(strtime)
    datetime=time.strftime('%Y-%m-%d %H:%M:%S', strtime)
    return datetime


