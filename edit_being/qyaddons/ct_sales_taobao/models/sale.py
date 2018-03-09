# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2012-today OSCG (<http://www.zhiyunerp.com>)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from odoo.osv import osv
from odoo import models, fields, api,_
from odoo.addons import decimal_precision as dp
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
from api.rest import CainiaoWaybillIiGetRequest
from api.rest import CainiaoCloudprintStdtemplatesGetRequest
import logging

_logger = logging.getLogger(__name__)

class product_template(models.Model):
    _inherit = 'product.template'
    num_iid= fields.Char(u'淘宝数字编码')


class product_product(models.Model):
    _inherit = 'product.product'
    sku_id=fields.Char(u'淘宝SKU_ID')





class sale_order(models.Model):
    _inherit = 'sale.order'


    buyer_memo=fields.Text(u'买家留言' )
    seller_memo=fields.Text(u'卖家留言' )
    slaes_type=fields.Selection(selection_add=
        [('taob', u'淘宝')])
    shop_id= fields.Many2one('taobao.shop', string=u"店铺",  readony = True)



class stock_picking(models.Model):
    _inherit = 'stock.picking'


    
    # 验证发货，更新电子面单
    def do_new_transfer(self):
        order = self.env['sale.order'].search([('name', '=', self.origin)])
        if not self.carrier_tracking_ref and order.slaes_type in ['taob']:
            # Receiver
            Receiver_Address = self.partner_id.street
            Receiver_CityName = self.partner_id.city
            Receiver_ExpAreaName = self.partner_id.street2
            Receiver_Mobile = self.partner_id.mobile
            Receiver_Name = self.partner_id.name
            Receiver_ProvinceName = self.partner_id.state_id.name

            # Send
            Send_self = self.picking_type_id.warehouse_id
            Send_Address = Send_self.partner_id.street
            Send_CityName = Send_self.partner_id.city
            Send_ExpAreaName = Send_self.partner_id.street2
            Send_Mobile = Send_self.partner_id.mobile
            Send_Name = Send_self.partner_id.name
            Send_ProvinceName = Send_self.partner_id.state_id.name

            appkey = order.shop_id.appkey
            secret = order.shop_id.appsecret
            url = order.shop_id.apiurl
            UserId = order.shop_id.UserId
            if order.shop_id.shop_id:  # 若有父级店铺则用父级的sessionkey 获取单号 ，否则用自己的
                father_id = self.env['taobao.shop'].search([('id', '=', order.shop_id.shop_id.id)])
                sessionkey = father_id.sessionkey
            else:
                sessionkey = order.shop_id.sessionkey
            port = 80

            setDefaultAppInfo(appkey, secret)
            req = TradeGetRequest(url, 80)
            req.fields = "tid,orders"
            req.tid =order.name
            resp = req.getResponse(sessionkey)
            if "error_response" in resp:
                raise osv.except_osv(u'警告', resp['error_response']['sub_msg'])
            else:
                status = resp['trade_get_response']['trade']['orders']['order'][0]['status']
                refund_status = resp['trade_get_response']['trade']['orders']['order'][0]['refund_status']
                NO1=0;NO2=0
                if refund_status != "NO_REFUND":  # 该订单存在退款
                    a=1
                else:
                    count=0
                    for ine in order.order_lin:
                        item_name=ine.product_id.name
                        count=ine.product_uom_qty+count
                    #对接菜鸟面单获取运单号
                    #获取打印模板ＵＲＬ
                    req = CainiaoCloudprintStdtemplatesGetRequest(url, port)
                    setDefaultAppInfo(appkey, secret)
                    resp = req.getResponse(sessionkey)
                    resilt =resp['cainiao_cloudprint_stdtemplates_get_response']['result']['datas']['standard_template_result'][0]
                    URL=resilt['standard_templates']['standard_template_do'][0]['standard_template_url']

                    #获取运单号
                    setDefaultAppInfo(appkey, secret)
                    req = CainiaoWaybillIiGetRequest(url, port)
                    req.param_waybill_cloud_print_apply_new_request = """
                    {"cp_code":'%s',
                    "sender":{"address":
                                {"city":"%s","detail":"%s","district":"%s","province":"%s"},
                                "mobile":"%s","name":"%s"},
                    "trade_order_info_dtos":{
                            "object_id":'20',
                             "order_info":{"order_channels_type":'TB',"trade_order_list":'%s'},
                              "package_info":{"id":'%s',"items":{"count":%s,"name":'%s'}},
                               "recipient":{"address":
                                {"detail":'%s',"province":'%s'},
                                 "mobile":'%s',"name":'%s'},
                                 "template_url":'%s',"user_id":'%s'
                       }
                    }
                    """ % (self.carrier_id.taob_code,Send_CityName,Send_Address,Send_ExpAreaName,Send_ProvinceName
                             ,Send_Mobile,Send_Name,order.name,self.name, count, item_name,
                           Receiver_Address, Receiver_ProvinceName, Receiver_Mobile, Receiver_Name,URL,UserId)
                    resp = req.getResponse(sessionkey)
                    print resp
                    if "error_response" in resp:
                        raise osv.except_osv(u'警告', resp['error_response']['sub_msg'])
                    else:
                        result = resp["cainiao_waybill_ii_get_response"]["modules"]["waybill_cloud_print_response"][0]
                        if result:
                            print_data = result['print_data']
                            datas = eval(print_data)
                            carrier_tracking_ref= datas['data']['waybillCode']  # 运单号
                            self.carrier_tracking_ref=carrier_tracking_ref
                            #发货
                            self.send_pick()


    def send_pick(self):
        order = self.env['sale.order'].search([('name', '=', self.origin)])
        secret= order.shop_id.secret
        appkey = order.shop_id.appkey
        sessionkey = order.shop_id.sessionkeysecret = order.shop_id.appsecret
        url = order.shop_id.apiurl
        carrier_tracking_ref = self.carrier_tracking_ref
        port = 80
        # 对接菜鸟面单获取运单号

        tid = order.order_num
        if "," in tid:
            x_a = tid.split(",")
            x = 0
            for x in x_a:
                if carrier_tracking_ref:
                    # 根据获取的运单号进行自动发货
                    setDefaultAppInfo(appkey, secret)
                    req = LogisticsOfflineSendRequest(url, port)
                    req.tid = x_a[x]
                    req.out_sid = carrier_tracking_ref  # 运单号
                    req.company_code = self.carrier_id.taob_code
                    resp = req.getResponse(sessionkey)
                    if "error_response" in resp:
                        raise osv.except_osv(u'警告', resp['error_response']['sub_msg'])
                    else:
                        jieguo = resp.get('logistics_offline_send_response').get('shipping', False)
                        succes = jieguo.get('is_success')

                        if succes:
                            super(stock_picking, self).do_new_transfer()
                        else:
                            raise osv.except_osv(u'警告', u"自动发货失败，请查看是否有异常数据")
                else:
                    raise osv.except_osv(u'警告', u"运单号异常，请进行查看")

        else:
            # 根据获取的运单号进行自动发货
            setDefaultAppInfo(appkey, secret)
            req = LogisticsOfflineSendRequest(url, port)
            req.tid = order.name
            req.out_sid = carrier_tracking_ref  # 运单号
            req.company_code = self.carrier_id.taob_code
            resp = req.getResponse(sessionkey)
            if "error_response" in resp:
                raise osv.except_osv(u'警告', resp['error_response']['sub_msg'])
            else:
                jieguo = resp.get('logistics_offline_send_response').get('shipping', False)
                succes = jieguo.get('is_success')
                if succes:
                    super(stock_picking, self).do_new_transfer()
                else:
                    raise osv.except_osv(u'警告', u"自动发货失败，请查看是否有异常数据")


class delivery(models.Model):
    _inherit = 'delivery.carrier'



    taob_code = fields.Char(string="代码")


class MergeWizard(osv.osv_memory):
    _inherit = 'ebiz.sale.merge.wizard'

    def merge_so(self,context=None):
        sale_obj = self.env['sale.order']
        order_line_obj = self.env['sale.order.line']
        sale_orders = []
        active_ids = context.get('active_ids',[])
        ship_name = False
        min_date_order = False
        min_date_order_so = False
        print active_ids
        if len(active_ids)<2:
            raise osv.except_osv(_('Warning'),_('Please select multiple order to merge in the list view.'))
        for so in sale_obj.browse(active_ids):
            if so.state == 'done' or so.state == 'cancel':# or so.shipped or so.invoiced:
                raise osv.except_osv(_('Warning'), _('You can not merge sale order in done or cancel state !'))
            #、收货人姓名、电话、手机、省份、城市、区县、地址相同，则认为是同一个联系人
            digest=so.partner_shipping_id
            key = "%s:%s:%s:%s:%s:%s:%s" % (digest.name, digest.phone, digest.mobile, digest.state_id.name,
                                            digest.city,digest.street2,digest.street)

            print ship_name
            print key
            if not ship_name:ship_name = key
            elif ship_name <> key:
                raise osv.except_osv(_('Warning'), _('You can not merge sale order with different shipping address !'))
            if not min_date_order:
                min_date_order = so.date_order #订单创建时间
                min_date_order_so = so #整条记录
            if min_date_order < so.date_order:
                min_date_order_so = so
            sale_orders.append(so)

        merge_so={
           # 'name': '%smg_%s' % (min_date_order_so.shop_id.code, self.env['ir.sequence'].get( 'sale.order') ),
            'name': 'mg_%s' % (self.env['ir.sequence'].get( 'sale.order') ),
            'shop_id': min_date_order_so.shop_id.id,
            'order_num':','.join(map(lambda x: x.name, sale_orders)),
            'date_order': min_date_order_so and min_date_order_so.date_order or False,
            'state': min_date_order_so.state,
            'partner_id':min_date_order_so and min_date_order_so.partner_id.id or False,
            'partner_invoice_id':min_date_order_so and min_date_order_so.partner_invoice_id and min_date_order_so.partner_invoice_id.id or False,
            'partner_shipping_id':min_date_order_so and min_date_order_so.partner_shipping_id and min_date_order_so.partner_shipping_id.id or False,
            'pricelist_id':min_date_order_so and min_date_order_so.pricelist_id.id or False,
        }
        so_id = sale_obj.create(merge_so)
        print so_id
        for so in sale_orders:
            for ln in so.order_line:
                vals = {
                    'order_id':so_id.id,
                    'product_id':ln.product_id.id or False,
                    'name':ln.name or '',
                    'product_uom_qty':ln.product_uom_qty or 1.00,
                    'product_uom':ln.product_uom.id or False,
                    'price_unit':ln.price_unit or 0.00,
                    'product_packaging':ln.product_packaging and ln.product_packaging.id or False,
                    'discount':ln.discount or 0.00,
                   # 'delay':ln.delay or False,
                }
                print vals
                order_line_obj.create(vals)

            self.env.cr.execute("""DELETE FROM sale_order where id='%s'""",(so.id,))
            self.env.cr.execute("""DELETE FROM sale_order_line where order_id='%s'""", (so.id,))
        return {'type': 'ir.actions.act_window_close'}


