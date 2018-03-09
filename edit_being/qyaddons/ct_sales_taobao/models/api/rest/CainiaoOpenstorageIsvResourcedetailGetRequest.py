'''
Created by auto_sdk on 2016.08.25
'''
from base import RestApi
class CainiaoOpenstorageIsvResourcedetailGetRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.isv_resource_id = None

	def getapiname(self):
		return 'cainiao.openstorage.isv.resourcedetail.get'
