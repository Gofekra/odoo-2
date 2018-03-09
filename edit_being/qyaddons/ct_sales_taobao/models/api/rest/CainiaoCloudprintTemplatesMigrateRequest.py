'''
Created by auto_sdk on 2016.09.19
'''
from base import RestApi
class CainiaoCloudprintTemplatesMigrateRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.custom_area_content = None
		self.custom_area_name = None
		self.tempalte_id = None

	def getapiname(self):
		return 'cainiao.cloudprint.templates.migrate'
