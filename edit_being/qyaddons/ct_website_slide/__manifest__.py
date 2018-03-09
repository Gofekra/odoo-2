# -*- coding: utf-8 -*-

{
    'name': 'Cotong video voice',
    'version': '1.0',
    'category': 'website',
    'summary': '	Share and Publish Videos, Presentations and Documents',
    'description': '',
    'author': 'Shanghai Cotong Software Co., Ltd.',
    'website': 'http://www.qitongyun.cn',
    'depends': [
        'web',
        'website_slides',
        'base_setup',
        'purchase'
    ],
    'data': [
        "views/views.xml",
        "views/slide.xml",
    ],
    "qweb": [
        "static/xml/slide_video.xml"
    ],
    'installable': True,
}
