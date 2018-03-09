'''
Created by auto_sdk on 2016.06.23
'''
from base import RestApi
class CainiaoCloudprintClientinfoPutRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.json_data = None

	def getapiname(self):
		return 'cainiao.cloudprint.clientinfo.put'
