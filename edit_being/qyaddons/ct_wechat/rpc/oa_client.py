# -*- coding: utf-8 -*-
from wechatpy import WeChatClient

client = None


def init_oa_client(appid, secret):
    global client
    client = WeChatClient(appid, secret)