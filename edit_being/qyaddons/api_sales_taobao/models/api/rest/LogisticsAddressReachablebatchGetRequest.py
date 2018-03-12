'''
Created by auto_sdk on 2016.07.04
'''
from base import RestApi
class LogisticsAddressReachablebatchGetRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.address_list = None

	def getapiname(self):
		return 'taobao.logistics.address.reachablebatch.get'
