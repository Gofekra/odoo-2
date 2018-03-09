# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.osv import osv
import xmlrpclib

class project_issue(models.Model):
    _inherit = 'project.issue'
    info_num=fields.Char(string="问题单号")
    feedback_demo=fields.Char(string="反馈账套")
    feedback_submitter=fields.Char(string='反馈者')
    feedback_submittpwd=fields.Char(string='反馈者密码')
    feedback_url=fields.Char(string="反馈地址")
    result_info=fields.Text(string="疑问解答")

    def send_info(self):
        feedback_demo=self.feedback_demo
        dbname = self.feedback_demo
        username='demo'
        pwd = 'aaa123'

        common = xmlrpclib.ServerProxy('{}/xmlrpc/2/common'.format(self.feedback_url))
        models = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(self.feedback_url))
        uid = common.authenticate(feedback_demo, username ,pwd, {})
        if uid:
            print self.info_num
            # 查询一条或多条记录,返回id
            args_id = models.execute(dbname, uid, pwd, 'question.info', 'search',  [('info_num', '=', self.info_num)])
            values = {
                'result_info': self.result_info
            }
            result1 = models.execute(self.feedback_demo, uid, pwd, 'question.info', 'write', args_id, values)

            if result1:
                return True
            else:
                return  False
        else:
            raise osv.except_osv(u'警告', "该问题的反馈者的身份存在问题，请联系管理员进行处理，"
                                        "\n 地址："+self.feedback_url+" \n 反馈账套："+self.feedback_demo+" \n 反馈者："+self.feedback_submitter)






