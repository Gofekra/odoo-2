# -*- coding: utf-8 -*-

import werkzeug
import urllib
import urllib2
import json

from odoo import http
from odoo.http import request


class SuppliersMap(http.Controller):

    @http.route(['/suppliersmap'], type='json', auth="public")
    def getPoint(self, marker_arr):
        points = []
        for marker in marker_arr:
            url = 'http://api.map.baidu.com/geocoder/v2/?' + 'address=' + marker['address'] + '&output=json&ak=K4VQM2n4iqE0kQZ0F8Y6HYdhfuGIktpB'
            url = url.encode("utf8")
            try:
                req = urllib2.Request(url)
                res_data = urllib2.urlopen(req)
                res = res_data.read()
                if res:
                    res = json.loads(res)
                    if res['status'] == 0:
                        lng = res['result']['location']['lng']
                        lat = res['result']['location']['lat']
                        points.append({'address': marker["address"], 'point': {'lng': lng, 'lat': lat}, 'name': marker["name"], 'tel': marker["tel"]})
            except Exception, e:
                pass          
        return points
