'''
Created by auto_sdk on 2016.05.22
'''
from base import RestApi
class WlbWmsItemCombinationDeleteRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.item_id = None

	def getapiname(self):
		return 'taobao.wlb.wms.item.combination.delete'
