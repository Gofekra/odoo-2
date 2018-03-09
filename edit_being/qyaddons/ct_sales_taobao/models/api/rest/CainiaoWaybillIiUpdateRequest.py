'''
Created by auto_sdk on 2016.07.01
'''
from base import RestApi
class CainiaoWaybillIiUpdateRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.param_waybill_cloud_print_update_request = None

	def getapiname(self):
		return 'cainiao.waybill.ii.update'
