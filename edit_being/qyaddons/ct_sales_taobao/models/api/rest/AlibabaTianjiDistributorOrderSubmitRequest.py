'''
Created by auto_sdk on 2016.01.04
'''
from base import RestApi
class AlibabaTianjiDistributorOrderSubmitRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.item_serial_no = None
		self.order_no = None
		self.product_serial_no = None

	def getapiname(self):
		return 'alibaba.tianji.distributor.order.submit'
