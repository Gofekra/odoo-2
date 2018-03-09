'''
Created by auto_sdk on 2016.09.19
'''
from base import RestApi
class CainiaoCloudprintStdtemplatesGetRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)

	def getapiname(self):
		return 'cainiao.cloudprint.stdtemplates.get'
