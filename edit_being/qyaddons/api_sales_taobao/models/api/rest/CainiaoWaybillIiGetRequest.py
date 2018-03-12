'''
Created by auto_sdk on 2016.09.12
'''
from base import RestApi
class CainiaoWaybillIiGetRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.param_waybill_cloud_print_apply_new_request = None

	def getapiname(self):
		return 'cainiao.waybill.ii.get'
