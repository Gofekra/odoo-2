# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request

class TreeviewController(http.Controller):

    @http.route('/treeview/order_test', type='json', auth="user")
    def get_test_data(self,key,val=[]):
        """位置数据存取"""
        treeview = request.env['ct.treeview']
        uid = request.env.uid
        getData = treeview.sudo().search([('name','=',key),('group_ids','=',uid)])
        if(getData):
            if(val):
                getData.sudo().write({'code':val})
            else:
                return getData[0].code
        else:
            if(val):
                treeview.sudo().create({'name':key,'code':val,'group_ids':uid})
        pass
        return []
