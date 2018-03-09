# -*- coding: utf-8 -*-
{
    'name': '业务伙伴地图',
    'category': 'website',
    'description': """
    主要内容:
    ----------------
    * 配置全局参数用于地图API，
    * 根据业务伙伴的地址显示百度地图坐标
    * 在首页显示本公司的地图坐标
        """,
    'version': '1.0',
    'author': 'Shanghai Cotong Software Co., Ltd.',
    'website': 'http://www.80sERP.com',
    'data': [
        "views/layoutone.xml",
        "views/res_company.xml",
    ],
    'category': 'Contact Baidu Map',
    'depends': ['website'],
}
