# -*- coding: utf-8 -*-

from odoo import models, fields, api,_
import datetime,time
import os,odoo,json
from odoo.exceptions import UserError, ValidationError
from . import  message

class DuMessage(models.Model):
    _name = 'mark.message'

    name = fields.Char(string="标题")
    context = fields.Many2one('template.message',string="发送内容")
    context_rel=fields.Text(string="" ,related='context.context',readonly="1")
    send_date=fields.Datetime(string="预约发起时间")
    partner_id = fields.Many2many('res.partner','mark_message_partner_id','message_oartner','partner_ids')
    state = fields.Selection([('draft', u'草稿'), ('send', u'已发送')],string='状态', default='draft')
    subject = fields.Selection([('lead', u'线索/商机'), ('customer', u'客户'), ('supplier', u'供应商'), ('custom', u'自定义')], string='筛选条件', default='custom')



    def commit_send_message(self,called,template_code,template_params):
        # msg_id
        # 用户自定义的短信ID，参数名必须填写，参数值可为空。
        # template_code
        # 模板编号
        # 短信模板编号，线下获取，请联系嘟嘟平台。模板格式：您好，您的验证码是{1}，{2}内有效。
        # template_params
        # 模板参数数组
        # 短信模板对应的参数数组，格式为["768768", "十分钟"]，每个参数的长度为40个字符，最多10个参数。数组中不可含有特殊字符[、]。

        res = self.env['message.config.settings'].get_default_info(None)
        # 定义常量
        app_key = str(res['app_key'])
        cust_account =str(res['cust_account'])
        org_tempKey =str(res['org_tempKey'])
        ext_terminalCode =str(res['ext_terminalCode'])
        msg_id=112
        data = message.send_message(app_key,cust_account,org_tempKey,ext_terminalCode,called,msg_id,template_code,template_params)
        return data

    def send_message(self):

        called=''
        for  partner_ids in self.partner_id:
           if partner_ids.phone:
               called+=partner_ids.phone+','
           elif  partner_ids.mobile:
               called += partner_ids.mobile + ','
        called=str(called[:-1])

        msg_id=112
        template_code='C91SSP'
        template_params=[called,"768768","10"]
        data = self.commit_send_message(called,template_code,template_params)


        sort_data = json.loads(data)
        print sort_data
        if sort_data['result'] == "0":
            self.state = 'send'

        else:
            raise UserError(_(sort_data['describe']))


class Template(models.Model):
    _name = 'template.message'

    name=fields.Char(string="标题")
    context=fields.Text(string="内容")



