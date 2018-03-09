'''
Created by auto_sdk on 2016.07.20
'''
from base import RestApi
class RegionPriceCancleRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.item_id = None
		self.sku_id = None

	def getapiname(self):
		return 'taobao.region.price.cancle'
