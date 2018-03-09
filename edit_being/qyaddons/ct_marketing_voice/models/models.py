# -*- coding: utf-8 -*-

from odoo import models, fields, api
from aip import AipSpeech
import datetime,time
import os,odoo,json
from . import dudu
from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.exceptions import UserError, ValidationError
from datetime import datetime, timedelta


class DuMessage(models.Model):
    _name = 'dudu.voice'

    def _compute_statistics(self):
        """ Compute statistics of the mass mailing """
        self.env.cr.execute("""
              SELECT
                  m.id as mailing_id,
                  COUNT(s.id) AS total,
                  COUNT(CASE WHEN s.receive is not null THEN 1 ELSE null END) AS receive,
                  COUNT(CASE WHEN s.send is not null THEN 1 ELSE null END) AS send,
                  COUNT(CASE WHEN s.replied is not null THEN 1 ELSE null END) AS replied,
                  COUNT(CASE WHEN s.failed is not null THEN 1 ELSE null END) AS failed
              FROM
                  dudu_voice_line s
              RIGHT JOIN
                  dudu_voice m
                  ON (m.id = s.voice_line_id)
              WHERE
                  m.id IN %s
              GROUP BY
                  m.id
          """, (tuple(self.ids),))
        for row in self.env.cr.dictfetchall():
            total = row.pop('total') or 1
            self.receive = 100.0 * row['receive'] / total
            self.send = 100.0 * row['send'] / total
            self.replied = 100.0 * row['replied'] / total
            self.failed = 100.0 * row['failed'] / total


    name = fields.Char(string="标题")
    send_type=fields.Selection([
        ('voice_message',u'语音通知'),
        ('voice_survey', u'语音调研'),
    ],string="发送类型",default="voice_message")
    context = fields.Many2one('template.voice',string="模板")
    context_rel=fields.Char(string="" ,related='context.context',readonly="1")
    send_date=fields.Datetime(string="预约发起时间")
    partner_id = fields.Many2many('res.partner','dudu_message_partner_id','message_oartner','partner_ids',string="客户")
    state = fields.Selection([('draft', u'草稿'), ('loading', u'发送中'), ('send', u'已发送'), ('canel', u'已取消')],string='状态', default='draft')
    subject = fields.Selection([('lead', u'标签列表'), ('customer', u'客户'), ('supplier', u'供应商'), ('custom', u'自定义')], string='筛选条件', default='custom',track_visibility='onchange')
    category_id=fields.Many2many('res.partner.category','voice_category_list','voice_category','category_voice',string='客户标签',track_visibility='onchange')
    receive = fields.Integer(compute="_compute_statistics",string="已接收")
    send = fields.Integer(compute="_compute_statistics", string="已发送")
    replied = fields.Integer(compute="_compute_statistics", string="已回复")
    failed= fields.Integer(compute="_compute_statistics", string="已失败")
    dudu_id=fields.One2many('dudu.voice.line','voice_line_id')
    batch_number=fields.Char(string="批次号")





    def unlink(self):
        for rec in self:
            if rec.state in ['loading','send']:
                raise   UserError(_("不能删除正在发送中或者已发送的语音记录"))
            else:
                return super(DuMessage,self).unlink()

    @api.model
    def create(self, vals):
        partner=vals['partner_id'][0][-1:]
        print partner
        for partner in partner[0]:
            print partner
            res=self.env['res.partner'].browse(partner)
            if not res.mobile and not res.phone :
                raise   UserError(_("发送对象的手机号或者电话不能同时为空"))


        if 'batch_number' in vals:
            vals['batch_number']='VO'+str(dudu.chartime())
        return super(DuMessage, self).create(vals)




    def write(self, vals):
        partner=vals['partner_id'][0][-1:]
        print partner
        for partner in partner[0]:
            print partner
            res=self.env['res.partner'].browse(partner)
            if not res.mobile and not res.phone :
                raise   UserError(_("发送对象的手机号或者电话不能同时为空"))
        return super(DuMessage, self).write(vals)




    def search_send(self):
        id=[]
        self.env.cr.execute("SELECT id FROM public.dudu_voice_line where send  is not null and voice_line_id=%s"  % (self.id))
        for status in self.env.cr.dictfetchall():
            id.append(int(status['id']))
        return {
            'name': '调研结果',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'tree',
            'res_model': 'dudu.voice.line',
            'view_id': self.env.ref('ct_marketing_voice.dudu_voice_line_tree').id,
            'domain': [('id', 'in', id)],
            'target': 'new'
        }

    def search_replied(self):
        id=[]
        self.env.cr.execute("SELECT id FROM public.dudu_voice_line where replied  is not null and voice_line_id=%s"  % (self.id))
        for status in self.env.cr.dictfetchall():
            id.append(int(status['id']))
        return {
            'name': '调研结果',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'tree',
            'res_model': 'dudu.voice.line',
            'view_id': self.env.ref('ct_marketing_voice.dudu_voice_line_tree').id,
            'domain': [('id', 'in', id)],
            'target': 'new'
        }
    def search_failed(self):
        id=[]
        self.env.cr.execute("SELECT id FROM public.dudu_voice_line where failed  is not null and voice_line_id=%s"  % (self.id))
        for status in self.env.cr.dictfetchall():
            id.append(int(status['id']))
        return {
            'name': '调研结果',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'tree',
            'res_model': 'dudu.voice.line',
            'view_id': self.env.ref('ct_marketing_voice.dudu_voice_line_tree').id,
            'domain': [('id', 'in', id)],
            'target':'new'
        }


    @api.onchange('subject','category_id')
    def _onchange_partner_id(self):
        if self.subject in ['lead']:#标签列表
            category=[]
            for category_id in self.category_id:
                category.append(category_id.id)
            print category
            return {
                'domain':{
                    'partner_id':[('category_id','in',category)]
                }
            }

        if self.subject in ['customer']:#客户
            return {
                'domain':{
                    'partner_id':[('customer','=',True)]
                }
            }

        if self.subject in ['supplier']:#供应商
            return {
                'domain':{
                    'partner_id':[('supplier','=',True)]
                }
            }

        if self.subject in ['custom']:#供应商
            return {
                'domain':{
                    'partner_id':[]
                }
            }

    def create_voice_line(self,sort_data):

            session_id = sort_data['session_id']
            voice_id=sort_data['voice_id']
            for voice_line in self.partner_id:
                session='';voice=''
                if voice_line.mobile:
                    session=session_id[voice_line.mobile]
                    voice=voice_id[voice_line.mobile]
                else:
                    session = session_id[voice_line.phone]
                    voice = voice_id[voice_line.phone]
                data={
                    'voice_line_id':self.id,
                    'customer_id': voice_line.id,
                    'phone':voice_line.phone,
                    'mobile': voice_line.mobile,
                    'send': datetime.now(),
                    'session_id':session,
                    'voice_id':voice

                }
                self.env['dudu.voice.line'].create(data)





    def draft_send_voice(self):
        for res in self.dudu_id:
            res.unlink()
        self.state='draft'
        self.batch_number='VO'+str(dudu.chartime())

    def canel_send_voice(self):
        res = self.env['audio.config.settings'].get_default_info(None)
        # 定义常量
        app_key = str(res['app_key'])
        cust_account =str(res['cust_account'])
        org_tempKey =str(res['org_tempKey'])
        ext_terminalCode =str(res['ext_terminalCode'])
        batch_number=str(self.batch_number)
        data = dudu.voice_canel(app_key, cust_account, ext_terminalCode, org_tempKey,batch_number)
        sort_data = json.loads(data)
        if sort_data['result'] == '0':
            self.state ='canel'
            for res in self.dudu_id:
                res.unlink()

        else:
            raise UserError(_(sort_data['describe']))


    def send_voice(self):
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        res = self.env['audio.config.settings'].get_default_info(None)
        # 定义常量
        app_key = str(res['app_key'])
        cust_account = str(res['cust_account'])
        org_tempKey = str(res['org_tempKey'])
        ext_terminalCode = str(res['ext_terminalCode'])
        called=''
        caller = '686016523'
        for  partner_ids in self.partner_id:
           if partner_ids.mobile:
               called+=partner_ids.mobile+','
           elif  partner_ids.phone:
               called += partner_ids.phone + ','
        called=str(called[:-1])
        batch_number=str(self.batch_number)
        if self.send_type in ['voice_message']:#语音通知
            tts_content="" #前导音

            mediaName=self.context.mediaName
            if self.send_date:
                schedule_send_time=(datetime.strptime(str(self.send_date),'%Y-%m-%d %H:%M:%S',) +timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S')
            else:
                schedule_send_time=None
            push_url=base_url+'/send_voice/'
            data = dudu.send_audio(app_key,cust_account,ext_terminalCode,mediaName,org_tempKey,
                                        caller,called,schedule_send_time,tts_content,push_url,batch_number)

            sort_data = json.loads(data)
            if sort_data['result'] == "0":
                sucss = self.create_voice_line(sort_data)
                self.state='send'

            else:
                raise UserError(_(sort_data['describe']))

        if self.send_type in ['voice_survey']:  # 语音调研
            mediaName=self.context.mediaName
            if self.send_date:
                startDate=(datetime.strptime(str(self.send_date),'%Y-%m-%d %H:%M:%S',) +timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S')
            else:
                startDate=None
            push_url=""

            data = dudu.voice_survey(app_key,cust_account,ext_terminalCode,mediaName,org_tempKey,
                                        caller,called,startDate,push_url,batch_number)

            sort_data = json.loads(data)
            print sort_data
            if sort_data['result'] == '0':
                self.create_voice_line(sort_data)
                self.state='send'
            else:
                raise UserError(_(sort_data['describe']))

    #查询调研结果
    def search_send_voice(self):
        res = self.env['audio.config.settings'].get_default_info(None)
        # 定义常量
        app_key = str(res['app_key'])
        cust_account =str(res['cust_account'])
        org_tempKey = str(res['org_tempKey'])
        product_key='IVVR'
        data = dudu.search_message_resault(app_key,cust_account,org_tempKey,product_key)
        sort_data = json.loads(data)
        print sort_data
        print sort_data['desc']
        print sort_data['exception']
        if sort_data['result'] == '0':
            date = sort_data.get('date')
            session_id = date['session_id']
            voice_id=date['voice_id']
            res = []
            for k in session_id:
                res.append(k)
            for res in res:
                voice_line = self.env['dudu.voice.line'].search(['&','&','|', ('phone', '=', str(res)), ('mobile', '=', str(res)),
                   ('session_id', '=', session_id[res]),('voice_id', '=', voice_id[res])])
            if voice_line:
                voice_line.replied = datetime.datetime.now()
                voice_line.voice_check = True
        else:
            raise UserError(_(sort_data['describe']))



class Voice_line(models.Model):
    _name = 'dudu.voice.line'

    customer_id=fields.Many2one('res.partner',string='客户')
    phone=fields.Char(string='手机')
    mobile=fields.Char(string='电话')
    digits=fields.Char(string="按键结果")
    voice_line_id=fields.Many2one('dudu.voice','dudu_id')
    receive = fields.Datetime(string="接收")
    send = fields.Datetime( string="发送")
    replied = fields.Datetime(string="回复")
    failed= fields.Datetime(string="失败")
    voice_check=fields.Boolean(string='调研成功')
    voice_id=fields.Char(string="存储编码")
    session_id=fields.Char(string="会话标识")


class Template(models.Model):
    _name = 'template.voice'

    def _compute_voice_url(self):

        strtime = time.localtime()
        datetime = time.strftime('%Y%m%d%H%M%S', strtime)
        Attachments = self.env['ir.attachment']
        for self in self:
            a = Attachments.search([('res_model','=',self._name), ('res_id','=',self.id), ('res_field','=','voice')])
            if a:
                print odoo.tools.config['data_dir']
            # if  self.voice:
            #     path = os.path.dirname(os.path.split(os.path.realpath(__file__))[0]) + '\\static\\audio\\' + datetime
            #     if not isinstance(self.voice, dict):
            #         with open(path+'.mp3', 'wb') as f:
            #             f.write(self.voice)
            #     self.write({'voice_url':"/ct_voice_marketing/static/audio/"+datetime+".mp3"})


    name=fields.Char(string="标题")
    context=fields.Char(string="内容")
    voice=fields.Binary(string="语音",track_visibility='onchange', attachment=True)
    voice_name=fields.Char(string="语音名称")
    mediaName=fields.Char(string="语音文件名称")
    voice_file=fields.Char(string="语音文件地址")
    voice_url=fields.Char(string="存储地址",compute="_compute_voice_url")

    url=fields.Char(string="url")
    state = fields.Selection([('draft', u'草稿'), ('complte', u'完成')], string='状态', default='draft')

    @api.model
    def search_url(self,id):
        res = self.env['template.voice'].search([('id', '=', id)])
        return res.url

    def change_voice(self,id):
        res=self.env['audio.config.settings'].get_default_info(None)
    # 定义常量
        APP_ID = res['APP_ID']
        API_KEY =  res['API_KEY']
        SECRET_KEY = res['SECRET_KEY']

        # 初始化AipSpeech对象
        aipSpeech = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

        result = aipSpeech.synthesis(self.context, 'zh', 1, {
            'vol': 5,
            # 'per':4
        })

        # 识别正确返回语音二进制 错误则返回dict 参照下面错误码

        strtime = time.localtime()
        datetime = time.strftime('%Y%m%d%H%M%S', strtime)
        path= os.path.dirname(os.path.split(os.path.realpath(__file__))[0])+'\\static\\audio\\'+datetime
        if not isinstance(result, dict):
            with open(path+'.mp3', 'wb') as f:
                f.write(result)

        self.write({'url':"/ct_marketing_voice/static/audio/"+datetime+".mp3"})
        self.write({'state':'complte'})




    #上传语音
    def commit_audio(self):
        res = self.env['audio.config.settings'].get_default_info(None)
        # 定义常量
        app_key = res['app_key']
        ext_orgCode = res['ext_orgCode']
        cust_account = res['cust_account']
        org_tempKey = res['org_tempKey']

        dudu.dudu.words_ro_audio()

    #上传文字
    def commit_message(self):
        res = self.env['audio.config.settings'].get_default_info(None)
        # 定义常量
        app_key = res['app_key']
        # ext_orgCode = res['ext_orgCode']
        cust_account = res['cust_account']
        org_tempKey = res['org_tempKey']
        ext_terminalCode = res['ext_terminalCode']

        content=self.context
        data=dudu.words_ro_audio(content,app_key,cust_account,org_tempKey,ext_terminalCode)

        sort_data = json.loads(data)
        if sort_data['result']=='0':
            self.mediaName=sort_data['mediaName']
            self.voice_file = sort_data['voice_file']
        else:
            raise UserError(_(sort_data['describe']))

