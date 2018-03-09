# -*- coding: utf-8 -*-

{
    'name': '企通云网站 建站模块增强包',
    'summary': '建站模块增强包',
    'category': 'Website',
    'author': 'Shanghai Cotong Software Co., Ltd.',
    'website': 'http://www.qitongyun.cn',
    'license': 'AGPL-3',
    'description': """
        1、修改头部点击事件
        2、增加底部的引导信息
        3、清除系统原始模块
        3、修改底部分享 分享内容标题获取网站标题 描述获取网站描述
    """,
    'depends': [
        'website',
    ],
    'data': [
        'views/config.xml',
        'views/assets.xml'
    ],
}