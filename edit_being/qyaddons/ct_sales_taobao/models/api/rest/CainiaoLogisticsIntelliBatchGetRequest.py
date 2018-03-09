'''
Created by auto_sdk on 2016.09.20
'''
from base import RestApi
class CainiaoLogisticsIntelliBatchGetRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.intelli_logistics_params = None

	def getapiname(self):
		return 'cainiao.logistics.intelli.batch.get'
