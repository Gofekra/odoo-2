'''
Created by auto_sdk on 2016.09.09
'''
from base import RestApi
class CainiaoWaybillprintClientupdateGetconfigRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.lan_ip = None
		self.mac = None
		self.msgid = None
		self.version = None

	def getapiname(self):
		return 'cainiao.waybillprint.clientupdate.getconfig'
