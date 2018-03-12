# -*- coding: utf-8 -*-
{
    'name': '语音营销',
    'category': 'Market',
    'summary': '语音营销',

    'description': """
    * 语音转化需要安装 pip install baidu-aip
    *  用户自写语音内容：语音会员群发、语音会员营销，单发、群发，
    *  支持行业及广告内营销内容
    *支持定时发送语音
""",
    'version': '1.0',
    'author': 'Gavin Gu',
    'website': '',
    'depends': [
        'base',
    ],
    'data': [
        "views/views.xml",
        "views/templates.xml",
        "views/audio_config_settings.xml",
    ],
    "qweb": [
        'static/xml/*.xml'
    ],
    'installable': True,
}
