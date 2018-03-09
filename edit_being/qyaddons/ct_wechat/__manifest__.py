# -*- coding: utf-8 -*-

{
    'name': '微信公众号管理',

    'category': 'Social Network',
    'summary': '微信公众号管理',

    'description': """
    * 需要pip安装wechatpy,pycrypto模块
    * 配置公众号参数，
    * 同步公众号联系人
    * 消息匹配自动回复
    * 指定人、组、标签进行群发消息
    * 关注自动回复消息并同步关注人信息
    * 为公众号创建菜单

    """,

    'version': '1.0',
    'author': 'Shanghai Cotong Software Co., Ltd.',
    'website': 'http://www.qitongyun.cn',
    'depends': ['web','auth_signup','ct_saas_users'],
    'application': True,
    'data': [
        'views/daili.xml',
        'views/confirm.xml',
        'views/parent_menus.xml',
        'views/wx_config_view.xml',
        'views/material_manage_view.xml',
        'views/autoreply_config_view.xml',
        'views/user_manage_view.xml',
        'views/wx_menu_item_middle_views.xml',
        'views/wx_menu_item_left_views.xml',
        'views/wx_menu_item_right_views.xml',
        'views/wx_menu_views.xml',
        'views/mass_message_view.xml',
    ],
    'qweb': [
    ],
    'installable': True,

}
