'''
Created by auto_sdk on 2016.08.25
'''
from base import RestApi
class TradeDrugOrdersGetRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.is_all_order = None
		self.is_all_shop = None
		self.keyword = None
		self.order_status = None
		self.page_no = None
		self.page_size = None
		self.shop_id = None

	def getapiname(self):
		return 'taobao.trade.drug.orders.get'
