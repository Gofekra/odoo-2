'''
Created by auto_sdk on 2016.07.07
'''
from base import RestApi
class InventoryWarehouseQueryRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.page_no = None
		self.page_size = None

	def getapiname(self):
		return 'taobao.inventory.warehouse.query'
