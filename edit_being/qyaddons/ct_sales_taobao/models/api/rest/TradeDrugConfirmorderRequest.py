'''
Created by auto_sdk on 2016.03.21
'''
from base import RestApi
class TradeDrugConfirmorderRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.confirm_type = None
		self.delivery_id = None
		self.order_id = None

	def getapiname(self):
		return 'taobao.trade.drug.confirmorder'
