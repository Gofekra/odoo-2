'''
Created by auto_sdk on 2016.06.12
'''
from base import RestApi
class WlbWmsUnknownPackageUploadRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.content = None

	def getapiname(self):
		return 'taobao.wlb.wms.unknown.package.upload'
