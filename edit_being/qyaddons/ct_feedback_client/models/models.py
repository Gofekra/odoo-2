# -*- coding: utf-8 -*-
from odoo import api, models, fields, SUPERUSER_ID, _
from odoo.exceptions import UserError, ValidationError
from odoo.osv import osv
import xmlrpclib


class Users(models.Model):
    _inherit = 'res.users'

    @api.model
    def get_current_user_email(self):
        return self.env.user.email


class FeedbackQuestion(models.Model):
    _name = 'ct_feedback_client.question'


    name = fields.Char(string='问题标题', translated=True)
    info_num = fields.Char(string="问题单号")
    email = fields.Char(string="电子邮件")
    description = fields.Char(string="问题描述")
    check_jind = fields.Char(string="跟踪进度")
    result_info = fields.Html(string="处理结果", translated=True)
    state = fields.Selection([('submitted','Submitted'), ('handled','Being Handled'), ('solved','Solved')], string='Status', default='submitted', translated=True)
    im_chanel_id = fields.Many2one('im_livechat.channel', string='')
    chat_url = fields.Char(name='Instant message channel', related='im_chanel_id.web_page', readonly=True, translated=True)

    # # 重写新建函数，生成流水号
    # def create_sequence(self,vals,):
    #     """ 创建序列号
    #     """
    #     seq = {'name': vals['prefix'], 'implementation': 'no_gap', 'prefix': vals['prefix'], 'padding': 3,
    #            'number_increment': 1}
    #     if 'company_id' in vals:
    #         seq['company_id'] = vals['company_id']
    #     yseq_id = self.env['ir.sequence'].sudo().search([('name', '=', seq['name'])])
    #     yflg = 0
    #     for rec in self.env['ir.sequence'].sudo().browse(yseq_id):
    #         yflg = 1
    #         break
    #     if yflg:
    #         return self.env['ir.sequence'].sudo().browse(yseq_id[0]).id
    #     else:
    #         return self.env['ir.sequence'].sudo().create(seq)

    # 重置创建函数添加一条新数据
    @api.model
    def create(self, vals):
        # users = self.pool.get('res.users').browse(cr, uid, uid, context=context)
        # if not 'sequence_id' in vals or not vals['sequence_id']:
        #     # 如果没有序列号，则新建
        #     prefix = str(fields.datetime.now().strftime('%Y%m%d'))
        #     vals.update({'prefix': prefix})
        #     vals.update({'sequence_id': self.create_sequence(vals).id})
        # # 获取流水号
        # vals['info_num'] = self.env['ir.sequence'].sudo().get_id(vals['sequence_id'])
        if 'info_num' not in vals:
            vals['info_num'] = self.env['ir.sequence'].sudo().next_by_code('question.info')
        if 'im_chanel_id' not in vals:
            vals['im_chanel_id'] = self.env['im_livechat.channel'].sudo().create({
                'name': vals['info_num'],
                'user_ids': [(6,0,[self.env.uid])],
            }).id
        return super(FeedbackQuestion, self).create(vals)


    @api.model
    def search_info(self):
        data = self.env['ct_feedback_client.question'].search([])
        res = []
        for data in data:
            res.append({
                'info_num':data.info_num,
                'name': data.name,
                'email': data.email,
                'description': data.description,
                'check_jind': data.check_jind,
                'result_info': data.result_info,
            })
        return res