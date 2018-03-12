# -*- coding: utf-8 -*-
{
    'name': 'Message Marketing',
    'version': '1.0',
    'category': '',
    'summary': '短信营销',
    'description': """
            用户自写短信内容：短信会员群发、短信会员营销
            单发、群发
            支持行业及广告内营销内容
            支持定时发送短信
    
            """,
    'author': 'Gavi Gu',
    'website': '',
    'depends': [
        'base',
    ],
    'data': [
        "views/views.xml",
        "views/message_config_settings.xml",
        "views/sms_config.xml",
    ],
    "qweb": [
    ],
    'installable': True,
}
