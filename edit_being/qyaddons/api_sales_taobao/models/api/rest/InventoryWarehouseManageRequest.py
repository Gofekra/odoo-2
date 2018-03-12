'''
Created by auto_sdk on 2016.07.07
'''
from base import RestApi
class InventoryWarehouseManageRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.ware_house_dto = None

	def getapiname(self):
		return 'taobao.inventory.warehouse.manage'
