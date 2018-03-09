# -*- encoding: utf-8 -*-
##############################################################################
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
"""
purCharse order import wizard
"""
import os
from odoo import models, fields, api
import time
from datetime import datetime, timedelta
import sys
import json
import logging
from dateutil.relativedelta import relativedelta
import urllib
import base64
import hashlib
from odoo.osv import osv
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
_logger = logging.getLogger(__name__)

class ebiz_product_sku_wizard(models.Model):
    _name = "ebiz.product.sku.wizard"
    # _description = u"商品匹配"

    date_start= fields.Datetime(u'修改时间(开始)' )
    date_end= fields.Datetime(u'修改时间(结束)')
    shop_id= fields.Many2one('taobao.shop', string=u"店铺", required=True)
    name=fields.Char(u'品名')
    product_ids=fields.One2many('ebiz.product.sku.line.wizard', 'product_id', u'商品列表')


    def search_product_sku(self):
        products = self.env['taobao.shop'].search_product(self.shop_id.id, self.name, self.date_start, self.date_end, )

        res = []
        for product in products:
            # raise osv.except_osv(u"aa" ,product.get('title'))
            out_code = ''
            if product.get('outer_id'):
                out_code = product.get('outer_id')
            num_code = str(product.get('num_iid')),
            name = product.get('title'),
            date_modified = product.get('modified'),
            pic_url = product.get('pic_url'),
            product_id = self.id

            code_id = self.env['ebiz.product.sku.line.wizard'].search( [('num_code', 'in', num_code)])
            if not code_id:
                self.env.cr.execute(
                    """INSERT INTO ebiz_product_sku_line_wizard(id, out_code, num_code, name, date_modified, product_id,shop_id,pic_url,state)
                    VALUES (nextval('ebiz_product_sku_line_wizard_id_seq'),%s, %s, %s, %s, %s, %s, %s,'1')""",
                    (out_code, num_code, name, date_modified, product_id, self.shop_id.id, pic_url))

class ebiz_product_sku_line_wizard(models.Model):
    _name = "ebiz.product.sku.line.wizard"
    _description = u"商品匹配列表"
    shop_id=fields.Many2one('taobao.shop', string=u"店铺", required=True)
    pic_url= fields.Char(u'商品图片')
    out_code=fields.Char(u'商家外部编码')
    num_code= fields.Char(u'商品数字编码')
    name=fields.Char(u'商品名称')
    date_modified= fields.Datetime(u'修改时间' )
    state=fields.Selection(
        [('1', u'草稿'), ('2', u'完成')], u'状态')
    product_id=fields.Many2one('ebiz.product.sku.wizard', u'商品匹配')



    def create_product(self,product_vals):
        """
        1) 创建product.template
        2) 如果商品有SKU，创建product.attribute, product.attribute.value，product.attribute.line
        3) 创建product.product
        4) 电商商品、SKU和ERP product.template、product.product的对应关系：
            如果没有SKU，则一个商品对应一个product.template、一个product.product，其中商品数字编码填入 product.template的num_iid，商家外部编码填入product.product的default_code，如果没有商家外部编码，则将num_iid填入default_code
            如果有SKU，则一个商品对应一个product.template，其中商品数字编码填入product.template的num_iid。每个SKU对应一个product.product，SKU的商家外部编码填入product.product的default_code，SKU的sku_id填入product.product的sku_id
        """
        def get_sku_properties(properties_name ):
            """SKU属性值格式  20000:3275069:品牌:盈讯;1753146:3485013:型号:F908;-1234:-5678:自定义属性1:属性值1
            返回结果 {'品牌':盈讯, '型号':F908, '自定义属性1':属性值1}
            """
            res = {}
            try:
                for vals in properties_name.split(';'):
                    v = vals.split(':')
                    res.update({v[2]: v[3] } )
            except Exception, e:
                pass
            return res

        product_res = []
        #创建Product Template 主产品

        def _compute_images(url):
            image=""
            if url:
                data = urllib.urlopen(url).read()
                image = base64.b64encode(data)

            return image

        vals_template = {
            'name': product_vals['name'],
            'num_iid': str(product_vals['num_iid']),
            'type': product_vals['type'],
            'list_price': product_vals['price'],
            'image_medium':_compute_images(product_vals['pic_url']),
            'cost_method': 'real',
            'standard_price': 1.0,
            'product_image_ids':[],
        }

        skus = product_vals.get('sku', False)
        prop_imglis=product_vals['prop_imglis']['url']
        vals_template_lin={}
        for url in prop_imglis:
            #Create table:product.imgae
            vals_template_lin={
                'name': product_vals['name'],
                'image': _compute_images(url),
            }

            vals_template['product_image_ids'].append((0, 0, vals_template_lin))

        if not skus:
            vals_template.update({'default_code': product_vals['default_code'] } )
            prt_ids = self.env['product.product'].create( vals_template)
            return [prt_ids]

        template_ids = self.env['product.template'].search( [('num_iid', '=', str(product_vals['num_iid']) )])
        if not template_ids:
            template_ids = self.env['product.template'].create(vals_template)
        else:
            template_ids = template_ids[0]

        #处理商品SKU
        attr_lines = {}
        for sku in skus:
            #创建 product.product
            if  "outer_id" in sku:
                default_code= sku['outer_id']
            else:
                default_code=""
            prt_vals = {
                'default_code': default_code,
                'sku_id': str(sku['sku_id']),
                'product_tmpl_id': template_ids.id,
                'attribute_value_ids': [],
            }

            #创建属性和属性值 product.attribute, product.attribute.value,
            #处理product.template上字段attribute_line_ids，对象product.attribute.line
            #处理product.product上字段attribute_value_ids
            properties = get_sku_properties(sku['properties_name'] )
            for k in properties:
                attr_ids = self.env['product.attribute'].search([('name', '=', k)])
                if attr_ids:
                    attr_ids = attr_ids[0]
                else:
                    attr_ids = self.env['product.attribute'].create({'name': k })

                attr_val_ids = self.env['product.attribute.value'].search([('name', '=', properties[k]), ('attribute_id', '=', attr_ids.id)])
                if attr_val_ids:
                    attr_val_ids = attr_val_ids[0]
                else:
                    self.env.cr.execute(
                        """INSERT INTO product_attribute_value(id, name, attribute_id)
                        VALUES (nextval('ebiz_product_sku_line_wizard_id_seq'),%s, %s)""",
                        (properties[k], attr_ids.id))
                    attr_val_ids = self.env['product.attribute.value'].search([('name', '=', properties[k]), ('attribute_id', '=', attr_ids.id)])

                prt_vals['attribute_value_ids'].append( (4, attr_val_ids.id) )
                if attr_ids not in attr_lines:
                    attr_lines[attr_ids] = {attr_val_ids: True}
                else:
                    attr_lines[attr_ids][attr_val_ids] = True

            #创建product.product
            prt_domain = []
            if prt_vals['default_code']:
                prt_domain = [ ('default_code', '=', prt_vals['default_code']) ]
            else:
                prt_domain = [ ('sku_id', '=', str(prt_vals['sku_id'])) ]
            prt_ids = self.env['product.product'].search( prt_domain)
            if prt_ids:
                prt_ids = prt_ids[0]
            else:
                #print prt_vals
                prt_ids = self.env['product.product'].create(prt_vals)

                #w为每个产品默认库位
                stock_quant={
                    'location_id':self.shop_id.stock_type.id,
                    'product_id':prt_ids.id,
                    'company_id':'1',
                    'qty':0.0
                }
                stock=self.env['stock.quant'].create(stock_quant)

            product_res.append(prt_ids)
        #
        # 重新创建product.attribute.line
        if attr_lines:
            attr_line_ids = self.env['product.attribute.line'].search( [('product_tmpl_id', '=', template_ids.id),('attribute_id', '=', attr_ids.id)])
            if attr_line_ids:
                self.env.cr.execute(
                    """DELETE FROM product_attribute_line where id='%s'""",
                    (attr_line_ids.id,))
               # self.env['product.attribute.line'].unlink(attr_line_ids.id)
            for attr in attr_lines:
                attr_line_vals = {
                    'product_tmpl_id':  template_ids.id,
                    'attribute_id': attr.id,
                    'value_ids': [],
                }
                for v in attr_lines[attr]:
                    attr_line_vals['value_ids'].append( (4, v.id) )
                attr_line_ids = self.env['product.attribute.line'].create(attr_line_vals)

        return product_res

    def import_product(self):
        """
        1) 按商品数字编码，取得商品SKU编码、属性和属性值
        2) 如果该商品没有SKU，且ERP中没有该商品，ERP中直接创建product.product
        3) 如果该商品有SKU，则ERP中创建product.template，且在product.template 上添加 属性和属性值，并且创建该SKU
        4) 电商店铺商品/SKU和ERP产品的对应关系：依次用电商商品/SKU的商家外部编码、商品数字编码、sku_id 匹配ERP产品的default_code, num_iid, sku_id
        5) 返回匹配的产品ids
        """

        for product in self:
            port = 80
            shop  = self.env['taobao.shop'].search([('id', '=',product.shop_id.id)])
            setDefaultAppInfo(shop.appkey, shop.appsecret)
           # req = ItemSkusGetRequest(shop.apiurl,port)
            req = ItemSellerGetRequest(shop.apiurl,port)
            # req.fields="sku_id, num_iid, properties, price, status, memo, properties_name, outer_id"
            req.fields = "num_iid,prop_img,sku,ku_id, num_iid, properties, price, status, memo, properties_name, outer_id,pic_url"
            res = []
           # req.num_iids = product.num_code
            req.num_iid = product.num_code
            resp= req.getResponse(shop.sessionkey)
            if "error_response" in resp:
                raise osv.except_osv(u'警告', resp['error_response']['sub_msg'])
            pic_url =  resp["item_seller_get_response"]["item"]['pic_url']
            num_iid =  resp["item_seller_get_response"]["item"]['num_iid']
            price =  resp["item_seller_get_response"]["item"]['price']
            prop_imglis ={
                'url':[]
            }
            if resp['item_seller_get_response']['item']['prop_imgs']:
                url=resp['item_seller_get_response']['item']['prop_imgs']['prop_img'] or False
                print resp['item_seller_get_response']['item']['prop_imgs']
                for url in url:
                    prop_imglis['url'].append(url['url'])
            else:
                url=""
            sku_lis = resp["item_seller_get_response"]["item"]["skus"]["sku"]
            product_vals = {
                'name': product.name,
                'num_iid': product.num_code,
                'type': 'product',
                'price': price ,
                'pic_url': pic_url,
                'default_code': product.out_code or product.num_code,
            }
            if  num_iid:
               # product_vals.update({'sku': skus.get('sku', False) })
                product_vals.update({'sku': sku_lis })
                product_vals.update({'prop_imglis': prop_imglis })
            ids = self.create_product( product_vals)
            res += ids
            self.write({'state':'2'})
            return res