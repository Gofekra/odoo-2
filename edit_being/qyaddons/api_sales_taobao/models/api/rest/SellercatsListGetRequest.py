'''
Created by auto_sdk on 2016.03.17
'''
from base import RestApi
class SellercatsListGetRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.fields = None
		self.nick = None

	def getapiname(self):
		return 'taobao.sellercats.list.get'
