'''
Created by auto_sdk on 2016.09.21
'''
from base import RestApi
class TradePostageUpdateRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.post_fee = None
		self.tid = None

	def getapiname(self):
		return 'taobao.trade.postage.update'
