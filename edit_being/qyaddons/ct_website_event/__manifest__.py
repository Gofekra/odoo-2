# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-

{
    'name': '企通云网站在线活动',
    'summary': '在线活动',
    'category': 'Website',
    'author': 'Shanghai Cotong Software Co., Ltd.',
    'website': 'http://www.qitongyun.cn',
    'license': 'AGPL-3',
    'summary': """
        企通云网站在线活动
    
      """,
    'description':  """
        企通云网站在线活动：
           页面底部增加分页
           分享活动
           访问量统计
           转化率统计
    """,
    'depends': ['base','event','website_event','ct_website_base'],


    'data': [
       'views/assets.xml',
        'views/website_event_template.xml',
        'views/config.xml',
        'views/views.xml',
    ],
}


