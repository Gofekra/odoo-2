'''
Created by auto_sdk on 2016.05.09
'''
from base import RestApi
class OcEserviceAppointListRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.code = None
		self.customer_nick = None
		self.customer_phone = None
		self.house_address_city = None
		self.mall_code = None
		self.seller_id = None
		self.sort_order = None
		self.start_appoint_time = None

	def getapiname(self):
		return 'taobao.oc.eservice.appoint.list'
