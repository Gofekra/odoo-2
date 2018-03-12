'''
Created by auto_sdk on 2016.05.06
'''
from base import RestApi
class OcEserviceAppointSaveRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.param_o2o_appoint_info_d_t_o = None

	def getapiname(self):
		return 'taobao.oc.eservice.appoint.save'
