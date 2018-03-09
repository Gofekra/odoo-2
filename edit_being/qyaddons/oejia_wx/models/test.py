# # -*- coding: utf-'8' "-*-"
import urllib2
import json
import func

APPID="wx231cd79cf1879388"
APPSECRET="c221fe45d679ddcfc3a8bb76e79a4ce0"
url="https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s" % (APPID,APPSECRET)

request = urllib2.Request(url)
get_data = urllib2.urlopen(request).read()
print get_data
sort_data = json.loads(get_data)
access_token= sort_data['access_token']



url1="https://api.weixin.qq.com/cgi-bin/menu/create?access_token=%s" % (access_token)
data={
    'button':
        [{'url': u'http://gwf.qitong.work/web#view_type=kanban&model=crm.team&action=234&menu_id=144',
          'type': 'view',
          'name': u'\u9500\u552e'}
         ]
}


request = urllib2.Request(url)
get_data = urllib2.urlopen(request).read()
sort_data = json.loads(get_data)
access_token= sort_data['access_token']

