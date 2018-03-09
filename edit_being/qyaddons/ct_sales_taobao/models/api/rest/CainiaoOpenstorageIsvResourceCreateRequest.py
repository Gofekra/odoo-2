'''
Created by auto_sdk on 2016.08.10
'''
from base import RestApi
class CainiaoOpenstorageIsvResourceCreateRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.param_create_isv_resource_request = None

	def getapiname(self):
		return 'cainiao.openstorage.isv.resource.create'
