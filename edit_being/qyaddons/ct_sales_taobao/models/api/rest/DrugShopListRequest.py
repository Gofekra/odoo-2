'''
Created by auto_sdk on 2016.08.25
'''
from base import RestApi
class DrugShopListRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.keywords = None
		self.page = None
		self.page_size = None
		self.status = None

	def getapiname(self):
		return 'taobao.drug.shop.list'
