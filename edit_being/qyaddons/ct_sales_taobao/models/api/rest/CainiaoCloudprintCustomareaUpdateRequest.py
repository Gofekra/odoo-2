'''
Created by auto_sdk on 2016.09.19
'''
from base import RestApi
class CainiaoCloudprintCustomareaUpdateRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.custom_area_content = None
		self.custom_area_id = None
		self.custom_area_name = None

	def getapiname(self):
		return 'cainiao.cloudprint.customarea.update'
