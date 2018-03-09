# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and licensing details.

{
    'name': 'ct_Lead_Chart',
    'category': 'Web',
    'summary': 'Funnel Chart for Leads & Opportunities',
    'author': 'Shanghai Cotong Software Co., Ltd.',
    'website': 'http://www.qitongyun.cn',
    'version': '10',
    'description': '线索、商机销售漏斗',
    'depends': [
        'crm'
    ],
    'data': [
        "views/templates.xml",
        "views/web_lead_funnel_chart_view.xml"
    ],
    'qweb': [
        'static/src/xml/*.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,

}
