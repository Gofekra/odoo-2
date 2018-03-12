# -*- coding: utf-8 -*-

{
    'name': 'Cotong video voice',
    'version': '1.0',
    'category': 'website',
    'summary': '	Share and Publish Videos, Presentations and Documents',
    'description': '',
    'author': 'Gavin Gu',
    'website': '',
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
