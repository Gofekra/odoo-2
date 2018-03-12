'''
Created by auto_sdk on 2016.04.08
'''
from base import RestApi
class DrugQuantityUpdateRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.out_item_id = None
		self.out_store_id = None
		self.quantity = None

	def getapiname(self):
		return 'taobao.drug.quantity.update'
