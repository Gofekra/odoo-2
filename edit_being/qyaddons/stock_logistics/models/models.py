# -*- coding: utf-'8' "-*-"
import urllib
import urllib2
import util
import urlparse
from odoo import api, fields, models
import controllers
from odoo.osv import osv
import  json


class stock_picking(models.Model):
    _inherit = 'stock.picking'

    message_id = fields.One2many('message.logistics', 'picking_id')
    rintptemplate = fields.Html(string="电子面单")
    desction=fields.Char(string="说明")


    def open_website_url(self):
        json_str = self.env['stock.logistics'].recognise(self.id)
        if json_str['Success'] == True and json_str['Traces']:
            message = json_str['Traces']
            message_id = self.env['message.logistics'].search([('picking_id', '=', int(self.id))])
            for unlink_id in message_id:
                unlink_id.unlink()

            for list in message:
                valus = {
                    'ftime': list['AcceptTime'],
                    'message': list['AcceptStation'],
                    'picking_id': int(self.id),
                }
                self.env['message.logistics'].create(valus)
        else:
            raise osv.except_osv(u'警告', json_str['Reason'])

    def do_new_transfer(self):
        if self.picking_type_code=='outgoing':
            print '############################'
            #手写快递单号进行发货
            if self.carrier_tracking_ref:
                # 订阅消息实时推送
                res = self.env['stock.logistics'].Subscription_push(self.id)
                return super(stock_picking, self).do_new_transfer()
            else:
                #电子面单API获取物流运单号
                res = self.env['stock.logistics'].get_number(self.id)
                search_message = json.loads(res)
                print search_message
                if search_message['Reason']=='成功':
                    LogisticCode=search_message['Order']['LogisticCode']
                    rintptemplate = search_message['PrintTemplate']
                    self.carrier_tracking_ref=LogisticCode
                    self.rintptemplate = rintptemplate
                    #订阅消息实时推送
                    res = self.env['stock.logistics'].Subscription_push(self.id)
                else:
                    raise osv.except_osv(u'警告', search_message['Reason'])
        return  super(stock_picking,self).do_new_transfer()#debug






class delivery(models.Model):
    _inherit = 'delivery.carrier'

    code = fields.Char(string="承运商代码")
    # api_code = fields.Many2one('stock.logistics',string= '物流接口')
    CustomerName=fields.Char(string="面单账号")
    CustomerPwd = fields.Char(string="面单密码")




