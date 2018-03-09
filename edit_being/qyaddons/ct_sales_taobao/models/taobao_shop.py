# -*- encoding: utf-8 -*-
import time
import logging
from odoo.tools import float_is_zero, float_compare
from dateutil.relativedelta import relativedelta
from datetime import datetime, timedelta
from odoo import models, fields, api,_
from odoo.osv import osv
import hashlib,json,urllib2, urllib, base64
import os
import uuid
import cookielib
from api.rest.base import setDefaultAppInfo
from api.rest import ItemsOnsaleGetRequest
from api.rest import TradesSoldIncrementGetRequest
from api.rest import ItemSkusGetRequest
from api.rest import TradesSoldGetRequest
from api.rest import TradeGetRequest
from api.rest import TradeFullinfoGetRequest
from api.rest import AlipayUserAccountreportGetRequest
from api.rest import ItemQuantityUpdateRequest
from api.rest import LogisticsOfflineSendRequest
from api.rest import ItemcatsGetRequest
from api.rest import ItemSellerGetRequest
import itertools
import logging
import re
import requests
_logger = logging.getLogger(__name__)


class taobao_shop(models.Model):
    _name = 'taobao.shop'
    _description = u"电商店铺"

    name=fields.Char(u'店铺名称', size=16, required=True)
    slaes_type=fields.Selection( [('taob', u'淘宝')], u'类型')
   # code=fields.Char(u'店铺前缀', size=8, required=True, help = u"系统会自动给该店铺的订单编号、客户昵称加上此前缀。通常同一个平台的店铺，前缀设置成一样")
    cp_code=fields.Selection([('YUNDA', u'韵达'), ('ZTO', u'中通'), ('STO', u'申通'),('SFO', u'顺丰')], u'快递')
    shop_id= fields.Many2one('taobao.shop', string=u"父级店铺")
    stock_type = fields.Many2one('stock.location', string=u"默认库位")
    appkey=fields.Char(u'App Key')
    appsecret=fields.Char(u'App Secret' )
    sessionkey=fields.Char(u'Session Key')
    apiurl= fields.Char(u'API URL' )
    UserId=fields.Char(u'UserId' )
    run= fields.Boolean(u'自动运行' )

    _defaults = {
        'slaes_type':'taob',
    }

    def search_product(self, ids, product_name=None, start_modified=None, end_modified=None):

        """
        1) 按商品名称，商品修改时间搜索店铺商品
        2) start_modified、end_modified 都是UTC时间，需要加上8小时传给电商平台
        """
        shop_id = self.env['taobao.shop'].search([('id', '=',ids)])
        setDefaultAppInfo(shop_id.appkey, shop_id.appsecret)
        req = ItemsOnsaleGetRequest(shop_id.apiurl, 80)
        req.fields = "approve_status,num_iid,title,nick, outer_id, modified,pic_url"
        if product_name:
            req.q = product_name
        if start_modified:
            start_modified = (
            datetime.strptime(str(start_modified), '%Y-%m-%d %H:%M:%S', ) + timedelta(hours=8)).strftime(
                '%Y-%m-%d %H:%M:%S')
            req.start_modified = start_modified
        if end_modified:
            end_modified = (datetime.strptime(str(end_modified), '%Y-%m-%d %H:%M:%S', ) + timedelta(hours=8)).strftime(
                '%Y-%m-%d %H:%M:%S')
            req.end_modified = end_modified

        req.page_no = 1
        req.page_size = 100
        total_get = 0
        total_results = 1000
        res = []
        while total_get < total_results:
            resp = req.getResponse(shop_id.sessionkey)
            print resp
            if "error_response" in resp:
                raise osv.except_osv(u'警告', resp['error_response']['sub_msg'])

            total_results = resp.get('items_onsale_get_response').get('total_results')

            if total_results > 0:
                res += resp.get('items_onsale_get_response').get('items').get('item')
            total_get += req.page_size
            req.page_no = req.page_no + 1
        #
        # 时间需要减去8小时
        for r in res:
            r['modified'] = (datetime.strptime(r['modified'], '%Y-%m-%d %H:%M:%S', ) - timedelta(hours=8)).strftime(
                '%Y-%m-%d %H:%M:%S')
        return res




    def search_import_orders(self,ids, status = 'WAIT_SELLER_SEND_GOODS', date_start = None, date_end = None):
            """
            搜索订单，批量导入
            """
            port = 80
            shop  = self.env['taobao.shop'].search([('id', '=',ids)])
            setDefaultAppInfo(shop.appkey, shop.appsecret)
            req = TradesSoldIncrementGetRequest(shop.apiurl,port)
            req.fields="seller_nick,buyer_nick,created,sid,tid,status,buyer_memo,seller_memo,payment,discount_fee,adjust_fee,post_fee,total_fee, pay_time,end_time,modified,received_payment,price,alipay_id,receiver_name,receiver_state,receiver_city,receiver_district,receiver_address, receiver_zip,receiver_mobile,receiver_phone,orders.price,orders.num,orders.iid,orders.num_iid,orders.sku_id,orders.refund_status,orders.status,orders.oid, orders.total_fee,orders.payment,orders.discount_fee,orders.adjust_fee,orders.sku_properties_name,orders.outer_iid,orders.outer_sku_id"
            req.status = status
            if date_start:
                date_start = (datetime.strptime(str(date_start), '%Y-%m-%d %H:%M:%S',) + timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S')
                req.start_modified = date_start
            if date_end:
                date_end = (datetime.strptime(str(date_end), '%Y-%m-%d %H:%M:%S',) + timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S')
                req.end_modified = date_end

            res = []
            req.page_no = 1
            req.page_size = 100
            total_get = 0
            total_results = 100
            while total_get < total_results:
                resp= req.getResponse(shop.sessionkey)
                trades = resp.get('trades_sold_increment_get_response').get('trades', False)
                total_results = resp.get('trades_sold_increment_get_response').get('total_results')
                if total_results > 0:
                    res += trades.get('trade')
                total_get += req.page_size
                req.page_no = req.page_no + 1

            # 时间需要减去8小时
            # 单号加上店铺前缀
            order_ids = []
            for trade in res:
                trade['created'] = (datetime.strptime(trade['created'], '%Y-%m-%d %H:%M:%S',) - timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S')
                trade['pay_time'] = (datetime.strptime(trade['pay_time'], '%Y-%m-%d %H:%M:%S',) - timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S')
                #trade['sale_code'] = '%s_%s' % (shop.code, trade['tid'])
                trade['sale_code'] =trade['tid']

            orders = self.remove_duplicate_orders(res)
            for trade in orders:
                partner_id, address_id = self.create_partner_address(trade )
                #创建订单及明细行
                order_id = self.create_order(shop, partner_id, address_id, trade)
                order_ids.append(order_id)
                # except Exception, e:
                #     #写入 同步异常日志
                #     syncerr = u"店铺【%s】订单【%s】同步错误: %s" % (shop.name, trade['tid'], e)
                #     self.pool.get('ebiz.syncerr').create({'name':syncerr, 'shop_id': shop.id, 'type': 'order', 'state': 'draft' }, context = context )
                #     continue
            return order_ids


    def remove_duplicate_orders(self, orders):
        sale_obj = self.env['sale.order']
        submitted_references = [o['sale_code'] for o in orders]
        existing_order_ids = sale_obj.search( [('name', 'in', submitted_references)])
        existing_orders = sale_obj.read(existing_order_ids, ['name'])
        existing_references = set([o['name'] for o in existing_orders])
        orders_to_save = [o for o in orders if o['sale_code'] not in existing_references]
        return orders_to_save




    def create_partner_address(self, trade):
        """
        1) 买家昵称和收货地址转变为 ERP的公司和联系人
        2) 判断Partner是否存在，不存在则创建
        3) 判断收货地址是否存在，不存在则创建
        4) 返回找到的，或者新建的 partner_id 和 address_id
        """
        partner_obj = self.env['res.partner']
        partner_name =trade.get('buyer_nick').strip()
        partner_ids = partner_obj.search([('name','=',partner_name),('is_company','=',True)] )
        if partner_ids:
            partner_ids = partner_ids[0]

           # bank_ids = self.env['res.partner.bank'].search([('partner_id','=',partner_ids.id),('acc_number','=',str(trade.get('alipay_id')).strip())],)
            bank_ids = self.env['res.partner.bank'].search([('acc_number','=',str(trade.get('alipay_id')).strip())],)
            if not bank_ids:
                bank_vals = self.env['res.partner.bank'].onchange_partner_id( [], partner_ids)['value']
                bank_vals.update({
                    'partner_id':partner_ids,
                    'acc_number':str(trade.get('alipay_id')).strip(),
                    'state': 'bank',
                    'bank_name': u'支付宝',
                    })
                self.env['res.partner.bank'].create(bank_vals,)
        else:
            bank_ids = self.env['res.partner.bank'].search([('acc_number','=',str(trade.get('alipay_id')).strip())],)
            if bank_ids:
                self.env.cr.execute(
                    """TE FROM res_partner_bank where id='%s'""",
                    (bank_ids.id,))
            country_id = self.env['res.country'].search([('code', '=', 'CN')] )
            bank_line_vals = {'state': 'bank','acc_number': str(trade.get('alipay_id')).strip(), 'bank_name': u'支付宝', }
            partner_val = {
                'name': partner_name,
                'is_company': True,
                'customer': True,
                'supplier': False,
                'bank_ids':[(0,0,bank_line_vals)],
                'country_id': country_id.id #and country_id[0],
            }
            partner_ids = partner_obj.create( partner_val)

        #检查收货地址，创建联系人
        #如果 买家昵称、收货人姓名、电话、手机、省份、城市、区县、地址相同，则认为是同一个联系人，否则ERP新建联系人
        addr_digest = "%s:%s:%s:%s:%s:%s:%s:%s" % (partner_name, trade.get('receiver_name', '').strip(), trade.get('receiver_phone', '').strip(), trade.get('receiver_mobile', '').strip(), trade.get('receiver_state', '').strip(), trade.get('receiver_city', '').strip(), trade.get('receiver_district', '').strip(), str(trade.get('receiver_address', '').strip()), )
        #addr_digest = hashlib.md5(addr_digest).digest()
        addr_ids = partner_obj.search([('digest', '=', addr_digest)])
        if addr_ids:
            addr_ids = addr_ids[0]
        else:
            country_id = self.env['res.country'].search([('name', '=', '中国')])
            state_id = country_id and self.env['res.country.state'].search( [('name', '=', trade.get('receiver_state', '').strip()), ('country_id', '=', country_id.id) ] )
            addr_val = {
                'parent_id': partner_ids.id,
                'name': trade.get('receiver_name', '').strip(),
                'phone': trade.get('receiver_phone', '').strip(),
                'mobile': trade.get('receiver_mobile', '').strip(),
                'country_id': country_id.id,# and country_id[0] ,
                'state_id': state_id.id,# and state_id[0],
                'city': trade.get('receiver_city', '').strip(),
                'street2': trade.get('receiver_district', '').strip(),
                'street': trade.get('receiver_address', '').strip(),

                'type': 'delivery',
                'digest': addr_digest,
                'use_parent_address': False,
                'is_company': False,
                'customer': False,
                'supplier': False,
            }
            addr_ids = partner_obj.create( addr_val)

        return [partner_ids, addr_ids]


    def create_order(self, shop, partner_id, address_id, trade):
        """
        1) 创建订单
        2) 创建明细行
        3) 添加邮费明细行
        4) 添加赠品明细行
        5) 添加优惠券明细行
        """
        order_obj = self.env['sale.order']
        line_obj = self.env['sale.order.line']
        order_val ={}
        addr =partner_id.address_get(['delivery', 'invoice'])
        order_val = {
            'pricelist_id':partner_id.property_product_pricelist and partner_id.property_product_pricelist.id or False,
            'payment_term_id': partner_id.property_payment_term_id and partner_id.property_payment_term_id.id or False,
            'partner_invoice_id': addr['invoice'],
            'partner_shipping_id': addr['delivery'],
        }

        if partner_id.user_id:
            order_val['user_id'] =partner_id.user_id.id
        if partner_id.team_id:
            order_val['team_id'] =partner_id.team_id.id


        order_val.update({
          # 'name': "%s_%s" % (shop.code,  trade.get('tid')),
           'name': trade.get('tid'),
            'shop_id': shop.id,
            'date_order':  trade.get('pay_time'),      #订单支付时间
            'create_date': trade.get('created'),       #订单创建时间
            'partner_id': partner_id.id,
            'partner_shipping_id': address_id.id,
            'buyer_memo': trade.get('buyer_memo'),
            'seller_memo': trade.get('seller_memo'),
            'picking_policy': 'one',
            'slaes_type': shop.slaes_type,
            'order_line': [],
        })

        orders = trade.get('orders', {}).get('order', [])
        for o in orders:
            prt_domain = [('default_code', '=', o.get('outer_iid', False)  or o.get('num_iid', False))]
            if o.get('sku_id', False):  #有SKU的情况
                if o.get('outer_sku_id', False):
                    prt_domain = [('default_code', '=', o.get('outer_sku_id', False) )]
                else:
                    prt_domain = [('sku_id', '=', o.get('sku_id', False) )]
            product_ids = self.env['product.product'].search( prt_domain )

            # #如果没有匹配到产品，报同步异常
            if product_ids:
            #     syncerr = u"订单导入错误: 匹配不到商品。tid=%s, 商品【%s】, outer_iid=%s, num_iid=%s, outer_sku_id=%s, sku_id=%s " % ( trade.get('tid'), o.get('title', ''), o.get('outer_iid', ''), o.get('num_iid', ''),  o.get('outer_sku_id', ''), o.get('sku_id', '') )
            #     self.pool.get('ebiz.syncerr').create(cr, uid, {'name':syncerr, 'shop_id':shop.id , 'type': 'order', 'state': 'draft' }, context = context )
            #     return False

            #添加订单明细行
                line_vals={}

                line_vals.update(
                    {
                    'product_id': product_ids.id ,
                    'name': product_ids.name ,
                    'product_uom': product_ids.uom_id.id ,
                     'price_unit':o.get('price'),
                     'product_uom_qty':o.get('num'),
                     } )
                order_val['order_line'].append( (0, 0, line_vals) )


       # print order_val
        order_id={}
        if order_val['order_line']:
            try:
                order_res = order_obj.search([('name', '=', order_val['name'])])
                if not order_res:
                    order_id = order_obj.create(order_val)
            except ValueError:
                a=1


            #自动确认订单
            # Automatic confirmation order
            for order in order_id:
                # 默认店铺快递
                sales_val = self.env['sale.order'].action_automatic(order)
                sales_id = self.env['stock.picking'].search([('origin', '=', order.name)])
                sales_id.cp_code = shop.cp_code
            if self.env['ir.values'].get_default('sale.config.settings', 'auto_done_setting'):
                self.action_done()

            return order_id


    def bt_seach(self):
        shop_id = self.env['taobao.shop'].search([('run', '=', True)])
        now_time = time.strftime('%Y-%m-%d %H:%M:%S')
        date_end = (datetime.strptime(str(now_time), '%Y-%m-%d %H:%M:%S', ) + timedelta(hours=8)).strftime( '%Y-%m-%d %H:%M:%S')
        date_start = (datetime.strptime(str(date_end), '%Y-%m-%d %H:%M:%S', ) - timedelta(hours=24)).strftime('%Y-%m-%d %H:%M:%S')
        for res in shop_id:
            ids=res.id
            orders = self.env['taobao.shop'].search_import_orders(ids, status='WAIT_SELLER_SEND_GOODS', date_start=date_start, date_end=date_end)





