'''
Created by auto_sdk on 2016.06.14
'''
from base import RestApi
class CainiaoCbossWorkplatformBiztypeQuerybyidRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.biz_type_id = None

	def getapiname(self):
		return 'cainiao.cboss.workplatform.biztype.querybyid'
