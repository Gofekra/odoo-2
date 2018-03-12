'''
Created by auto_sdk on 2016.06.14
'''
from base import RestApi
class CainiaoCbossWorkplatformBiztypeQueryallRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.level = None
		self.trade_id = None

	def getapiname(self):
		return 'cainiao.cboss.workplatform.biztype.queryall'
