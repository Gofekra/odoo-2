'''
Created by auto_sdk on 2016.07.01
'''
from base import RestApi
class CainiaoWaybillIiQueryByWaybillcodeRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.param_list = None

	def getapiname(self):
		return 'cainiao.waybill.ii.query.by.waybillcode'
