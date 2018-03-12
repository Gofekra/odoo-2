'''
Created by auto_sdk on 2016.06.22
'''
from base import RestApi
class CainiaoWaybillIiProductRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.cp_code = None

	def getapiname(self):
		return 'cainiao.waybill.ii.product'
