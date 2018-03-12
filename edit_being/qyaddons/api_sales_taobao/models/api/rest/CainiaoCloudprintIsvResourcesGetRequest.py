'''
Created by auto_sdk on 2016.09.19
'''
from base import RestApi
class CainiaoCloudprintIsvResourcesGetRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.isv_resource_type = None

	def getapiname(self):
		return 'cainiao.cloudprint.isv.resources.get'
