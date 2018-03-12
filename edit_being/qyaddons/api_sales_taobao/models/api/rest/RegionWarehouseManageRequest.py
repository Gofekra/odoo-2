'''
Created by auto_sdk on 2016.07.14
'''
from base import RestApi
class RegionWarehouseManageRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.regions = None
		self.store_code = None

	def getapiname(self):
		return 'taobao.region.warehouse.manage'
