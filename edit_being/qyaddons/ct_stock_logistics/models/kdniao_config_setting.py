# -*- coding: utf-'8' "-*-"
import json
import urllib
import urllib2
import hashlib
import base64
import urllib

from odoo import api, fields, models
from odoo.osv import osv

class logistics(models.Model):
    _name = 'stock.logistics'
    _inherit = 'res.config.settings'


    name = fields.Char(string="API名称")
    key = fields.Char(string="授权key")
    customer = fields.Char(string='customer ID')
    secret = fields.Char(string='secret')
    _rec_name="name"

    def get_default_appid(self,fields):
        Param = self.env["ir.config_parameter"]
        return {
            'key': Param.get_param('key', default='be6fdf4f-64f2-45f6-ac15-faf6b97378b4'),
            'customer': Param.get_param( 'customer', default='1285595'),
            'secret': Param.get_param('secret',default=''),
        }

    def set_appid(self):
        Param = self.env["ir.config_parameter"]
        Param.set_param( 'key', self.key)
        Param.set_param( 'customer', self.customer)
        Param.set_param( 'secret', self.secret)


    def url(self):
         url="http://api.kdniao.cc/Ebusiness/EbusinessOrderHandle.aspx"

    def encrypt(self,origin_data, appkey):
        """数据内容签名：把(请求内容(未编码)+AppKey)进行MD5加密，然后Base64编码"""
        m = hashlib.md5()
        m.update((origin_data+appkey).encode("utf8"))
        encodestr = m.hexdigest()
        base64_text = base64.b64encode(encodestr.encode(encoding='utf-8'))
        return base64_text

    def sendpost(self,url, datas):
        """发送post请求"""
        postdata = urllib.urlencode(datas).encode('utf-8')

        header = {
            "Accept": "application/x-www-form-urlencoded;charset=utf-8",
            "Accept-Encoding": "utf-8"
        }
        req = urllib2.Request(url, postdata, header)
        get_data = (urllib2.urlopen(req).read().decode('utf-8'))
        return get_data



    def get_traces(self,logistic_code, shipper_code, appid, appkey, url):
        """查询接口支持按照运单号查询(单个查询)"""
        data1 = {'LogisticCode': logistic_code, 'ShipperCode': shipper_code}
        d1 = json.dumps(data1, sort_keys=True)
        requestdata =self.encrypt(d1, appkey)
        post_data = {'RequestData': d1, 'EBusinessID': appid, 'RequestType': '1002', 'DataType': '2',
                     'DataSign': requestdata.decode()}
        json_data = self.sendpost(url, post_data)
        sort_data = json.loads(json_data)
        print sort_data
        return sort_data


    def get_company(self,logistic_code, appid, appkey, url):
        """获取对应快递单号的快递公司代码和名称"""
        data1 = {'LogisticCode': logistic_code}
        d1 = json.dumps(data1, sort_keys=True)
        requestdata = self.encrypt(d1, appkey)
        post_data = {
            'RequestData': d1,
            'EBusinessID': appid,
            'RequestType': '2002',
            'DataType': '2',
            'DataSign': requestdata.decode()}
        json_data = self.sendpost(url, post_data)
        sort_data = json.loads(json_data)
        return sort_data


    def recognise(self,id):
        """查询输出数据"""
       # url = 'http://testapi.kdniao.cc:8081/Ebusiness/EbusinessOrderHandle.aspx'
        url = "http://api.kdniao.cc/Ebusiness/EbusinessOrderHandle.aspx"
        valus = self.env['stock.picking'].search([('id', '=', id)])
        expresscode = valus.carrier_tracking_ref
        data = self.get_default_appid(fields)
        key = data['key']
        EBusinessID = data['customer']

        if valus.carrier_id:
            trace_data = self.get_traces(expresscode, valus.carrier_id.code, EBusinessID, key, url)
        else:
            data = self.get_company(expresscode, EBusinessID, key, url)
            trace_data={}
            if data['ShipperCode']:
                if data['Success'] == False:
                       Reason=data['Reason']
                else:
                   trace_data = self.get_traces(expresscode, data['Shippers'][0]['ShipperCode'], EBusinessID, key, url)
            else:
                raise osv.except_osv(u'警告', "未能识别该单号")
        return trace_data



    def get_number(self,id):
            #########################
            #电子面单字段解释：
            #CallBack 用户自定义回调信息
            #Commodity 商品信息 { GoodsCode：商品编码   GoodsDesc：商品描述   GoodsName：商品名称  GoodsPrice商品价格  Goodsquantity：商品数量
            # GoodsVol:商品体积M3   GoodsWeight:商品重量}
            #Cost：运费  CustomerName：电子面单客户账号    CustomerPwd：密码  StartDate- EndDate：上门取货时间段  ExpType：快件类型（默认为标准快件）
            #IsNotice 是否通知上门取件【0：通知】  IsReturnPrintTemplate 返回单子面单模板【0：不需要】  LogisticCode：快递单号
            #MemberID 会员标识【平台方与快递鸟统一用户标识的商家ID】  MonthCode月结编码   OrderCode：订单编码  OtherCost：其他费用
            #PayType 快递费付款方【1：寄 2：收】  Quantity：件数/包裹数
            #Receiver 收件人信息{ Address：地址  CityName：市  ExpAreaName：区  Mobile：电话  Name：收件人  ProvinceName：市}
            #Remark：备注
            #Sender 寄件人信息{ Address：地址  CityName：市  ExpAreaName：区  Mobile：电话  Name：寄件人  ProvinceName：市 }
            #SendSite：收件网点标识  ShipperCode：快递公司编码  Volume：物品总体积   Weight：物品总重量

            valus=self.env['stock.picking'].search([('id','=',id)])
            LogisticCode = valus.carrier_tracking_ref

            data=self.get_default_appid(fields)

            key = data['key']
            EBusinessID = data['customer']

            OrderCode=valus.name
            GoodsName=valus.move_lines.product_id.name

            ShipperCode=valus.carrier_id.code
            CustomerName = valus.carrier_id.CustomerName
            CustomerPwd = valus.carrier_id.CustomerPwd

            #Receiver
            Receiver_Address=valus.partner_id.street
            Receiver_CityName=valus.partner_id.city
            Receiver_ExpAreaName=valus.partner_id.street2
            Receiver_Mobile=valus.partner_id.mobile
            Receiver_Name=valus.partner_id.name
            Receiver_ProvinceName=valus.partner_id.state_id.name

            #Send
            Send_valus=valus.picking_type_id.warehouse_id
            Send_Address = Send_valus.partner_id.street
            Send_CityName = Send_valus.partner_id.city
            Send_ExpAreaName = Send_valus.partner_id.street2
            Send_Mobile = Send_valus.partner_id.mobile
            Send_Name = Send_valus.partner_id.name
            Send_ProvinceName = Send_valus.partner_id.state_id.name
            url = 'http://api.kdniao.cc/api/EOrderService'
            data1= {"CallBack": OrderCode, "Commodity": [
                  {"GoodsCode": "", "GoodsDesc": "", "GoodsName": GoodsName, "GoodsPrice": "", "Goodsquantity": "",
                   "GoodsVol": "", "GoodsWeight": ""}], "Cost": "", "CustomerName": CustomerName, "CustomerPwd": CustomerPwd,
            "EndDate": "", "ExpType": "1", "IsNotice": "0", "IsReturnPrintTemplate": "1", "LogisticCode": LogisticCode,
            "MemberID": "", "MonthCode": "", "OrderCode": OrderCode, "OtherCost": "", "PayType": "1", "Quantity": "",
            "Receiver": {"Address": Receiver_Address, "CityName": Receiver_CityName, "ExpAreaName": Receiver_ExpAreaName, "Mobile": Receiver_Mobile,
                         "Name": Receiver_Name, "ProvinceName": Receiver_ProvinceName}, "Remark": "",
            "Sender": {"Address": Send_Address, "CityName":Send_CityName, "ExpAreaName":Send_ExpAreaName, "Mobile":Send_Mobile,
                       "Name": Send_Name, "ProvinceName": Send_ProvinceName}, "SendSite": "", "ShipperCode":ShipperCode, "StartDate": "",
            "Volume": "", "Weight": ""}


            d1 = json.dumps(data1, sort_keys=True)
            requestdata =self.encrypt(d1, key)
            post_data = {'RequestData': d1, 'EBusinessID': EBusinessID, 'RequestType': '1007', 'DataType': '2',
                            'DataSign': requestdata.decode()}
            json_data = self.sendpost(url, post_data)
            return json_data



    def Subscription_push(self,id):
        #url = 'http://testapi.kdniao.cc:8081/Ebusiness/EbusinessOrderHandle.aspx'
        url = "http://api.kdniao.cc/Ebusiness/EbusinessOrderHandle.aspx"
        valus = self.env['stock.picking'].search([('id', '=', id)])
        OrderCode = valus.name
        LogisticCode = valus.carrier_tracking_ref

        data = self.get_default_appid(fields)
        key = data['key']
        EBusinessID = data['customer']

        data = self.get_company(LogisticCode, EBusinessID, key, url)
        if data['Shippers'][0]:
            ShipperCode=data['Shippers'][0]['ShipperCode']
            data= {"CallBack": OrderCode, "IsNotice": "0", "LogisticCode": LogisticCode, "MemberID": "", "OrderCode": OrderCode,
             "Receiver": {"Address": "", "CityName": "", "ExpAreaName": "", "Mobile": "", "Name": "", "ProvinceName": ""},
             "Sender": {"Address": "", "CityName": "", "ExpAreaName": "", "Mobile": "", "Name": "", "ProvinceName": ""},
             "ShipperCode": ShipperCode}

            d1 = json.dumps(data, sort_keys=True)
            requestdata = self.encrypt(d1, key)
            post_data = {'RequestData': d1, 'EBusinessID': EBusinessID, 'RequestType': '1008', 'DataType': '2',
                         'DataSign': requestdata.decode()}
            json_data = self.sendpost(url, post_data)
        return json_data

class message_logistics(models.Model):
    _name = 'message.logistics'
    ftime= fields.Char(string="时间")
    message = fields.Char(string="地点和跟踪进度")
    picking_id = fields.Many2one('stock.picking','message_id')
    _order="ftime desc"



















