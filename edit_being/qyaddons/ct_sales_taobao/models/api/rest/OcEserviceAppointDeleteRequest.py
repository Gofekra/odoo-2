'''
Created by auto_sdk on 2016.05.09
'''
from base import RestApi
class OcEserviceAppointDeleteRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.code = None
		self.seller_id = None

	def getapiname(self):
		return 'taobao.oc.eservice.appoint.delete'
