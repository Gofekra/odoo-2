'''
Created by auto_sdk on 2014.07.21
'''
from base import RestApi
class ShoprecommendItemsGetRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.count = None
		self.ext = None
		self.recommend_type = None
		self.seller_id = None

	def getapiname(self):
		return 'taobao.shoprecommend.items.get'
