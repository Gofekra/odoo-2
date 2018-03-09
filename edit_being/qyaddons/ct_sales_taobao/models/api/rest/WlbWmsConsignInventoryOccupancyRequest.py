'''
Created by auto_sdk on 2016.05.25
'''
from base import RestApi
class WlbWmsConsignInventoryOccupancyRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.content = None

	def getapiname(self):
		return 'taobao.wlb.wms.consign.inventory.occupancy'
