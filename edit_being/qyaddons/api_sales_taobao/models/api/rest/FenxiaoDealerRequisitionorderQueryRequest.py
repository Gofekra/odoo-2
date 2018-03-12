'''
Created by auto_sdk on 2016.07.11
'''
from base import RestApi
class FenxiaoDealerRequisitionorderQueryRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.dealer_order_ids = None
		self.fields = None

	def getapiname(self):
		return 'taobao.fenxiao.dealer.requisitionorder.query'
