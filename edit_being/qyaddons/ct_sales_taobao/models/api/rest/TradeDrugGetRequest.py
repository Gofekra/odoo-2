'''
Created by auto_sdk on 2016.03.21
'''
from base import RestApi
class TradeDrugGetRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.is_all = None
		self.max_size = None
		self.store_id = None

	def getapiname(self):
		return 'taobao.trade.drug.get'
