# -*- coding: utf-8 -*-
{
    'name': "淘宝订单管理",

    'summary': """
        对接淘宝
        
        """,
    'description': """
    1) 淘宝等电商网店的订单导入
    2) 自动开发票，验证付款、确认销售
    3) 订单的运单号回写到电商网店
    4) 自动为订单开Invoice，自动确认，形成应付账款
    5) 自动导入电商网店的对账单
    """,

    'author': "Gavin Gu",
    'website': "http://www.qitongyun.cn/",
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','sale', 'stock_account', 'delivery','ct_sales'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/templates.xml',
        'views/ebiz_product_sku_wizard.xml',
        'views/ebiz_check_order_wizard.xml',
        'views/taobao_shop.xml',
        'views/ebiz_view.xml',

    ],
    'demo': [
        'demo/demo.xml',
    ],
    'installable': True,
    'active': False,
    'application': False,
}

