'''
Created by auto_sdk on 2016.05.30
'''
from base import RestApi
class ItemGetRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.fields = None
		self.num_iid = None

	def getapiname(self):
		return 'taobao.item.get'
