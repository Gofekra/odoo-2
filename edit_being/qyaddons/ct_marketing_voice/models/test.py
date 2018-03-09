# # # -*- coding:utf-8 -*-
# import os
#
# print os.getcwd()
# print os.path.dirname(os.getcwd())
import json


data='{"data":[{"app_key":"420BAF8109315644921908D7D9EC6E45","callee":"13578503881","cust_account":"qitongyun","digits":"1","session_id":"acb345d2-5bee-4962-a393-49df8cbed3a9"}],"describe":"请按照文档接口回复"} '

params = json.loads(data)
print params
print params['data']




