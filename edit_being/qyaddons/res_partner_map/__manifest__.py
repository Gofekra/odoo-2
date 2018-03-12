# -*- coding: utf-8 -*-
{
    'name': 'Cotong Partner Map',
    'version': '1.0',
    'category': 'MAP',
    'summary': '业务伙伴百度地图',
    'description': '',
    'author': 'Shanghai Cotong Software Co., Ltd.',
    'website': 'http://www.qitongyun.cn',
    'depends': [
        'web',
        'purchase',
        'base_setup'
    ],
    'data': [
        "views/map.xml",
        "views/partner_map.xml"
    ],
    "qweb": [
        "static/src/xml/baidu_map.xml"
    ],
    'installable': True,
}
