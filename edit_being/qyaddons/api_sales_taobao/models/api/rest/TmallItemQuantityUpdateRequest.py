'''
Created by auto_sdk on 2016.02.02
'''
from base import RestApi
class TmallItemQuantityUpdateRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.item_id = None
		self.item_quantity = None
		self.options = None
		self.sku_quantities = None

	def getapiname(self):
		return 'tmall.item.quantity.update'
