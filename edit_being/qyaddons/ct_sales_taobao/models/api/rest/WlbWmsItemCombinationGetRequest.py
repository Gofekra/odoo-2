'''
Created by auto_sdk on 2016.05.17
'''
from base import RestApi
class WlbWmsItemCombinationGetRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.itemid = None

	def getapiname(self):
		return 'taobao.wlb.wms.item.combination.get'
