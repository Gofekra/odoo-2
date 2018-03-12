'''
Created by auto_sdk on 2016.08.25
'''
from base import RestApi
class CainiaoOpenstorageSellerResourcedetailGetRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.seller_resource_id = None

	def getapiname(self):
		return 'cainiao.openstorage.seller.resourcedetail.get'
