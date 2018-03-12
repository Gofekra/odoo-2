'''
Created by auto_sdk on 2016.03.21
'''
from base import RestApi
class DeliveryDrugPickupRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.delivery_order_no = None
		self.latitude = None
		self.longitude = None

	def getapiname(self):
		return 'taobao.delivery.drug.pickup'
