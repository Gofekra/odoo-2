'''
Created by auto_sdk on 2016.09.07
'''
from base import RestApi
class WlbWmsStockOutOrderConfirmRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.content = None

	def getapiname(self):
		return 'taobao.wlb.wms.stock.out.order.confirm'
