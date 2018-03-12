'''
Created by auto_sdk on 2016.04.08
'''
from base import RestApi
class DrugPriceUpdateRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.out_item_id = None
		self.out_store_id = None
		self.price = None

	def getapiname(self):
		return 'taobao.drug.price.update'
