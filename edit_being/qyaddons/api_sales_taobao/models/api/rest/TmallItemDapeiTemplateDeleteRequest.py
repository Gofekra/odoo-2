'''
Created by auto_sdk on 2016.07.06
'''
from base import RestApi
class TmallItemDapeiTemplateDeleteRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.id = None

	def getapiname(self):
		return 'tmall.item.dapei.template.delete'
