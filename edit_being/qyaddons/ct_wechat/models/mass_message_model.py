# -*- coding: utf-8 -*-
from odoo import models, fields, api,SUPERUSER_ID
from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.exceptions import UserError, ValidationError
from autoreply_model import REPLY_CONTENT
from ..rpc import oa_client

CONTENT_SEND = [
		('wx.image', '图片'),
		('wx.text', '文字'),
        ('wx.imagetext', '单图文'),
        ('wx.many.imagetext', '多图文'),
	]


class MassMessage(models.Model):
    _name = 'wx.mass.message'

    name = fields.Char('名称')
    content= fields.Reference(string='内容',selection=CONTENT_SEND)
    state = fields.Selection([('1', '未发送'), ('2', '已发送'),('3', '已删除')],
                             string='发送状态', default='1', readonly=True)
    send_date = fields.Char(string='发送时间', readonly=True)
    user_ids = fields.Many2many( 'wx.user', id1='tag_id', id2='user_id', string='指定收件人')
    mass_tags = fields.Many2many('wx.tag', string='按标签选择')
    mass_sex = fields.Selection(
        [(3, u'全部'), (1, u'男'), (2, u'女')], string=u'性别', default=3)
    city = fields.Char(u'城市')
    province = fields.Char(u'省份')
    country = fields.Char(u'国家')
    msg_id=fields.Char(string="消息ID")



    def delete_mess(self):
        message = oa_client.client.message.delete_mass(self.msg_id)
        errcode = message['errcode']
        if errcode == 0:
            self.state = '3'
        else:
            raise UserError(_(message['errmsg']))



    def search_mess_state(self):
        # message = oa_client.client.message.get_mass(self.content.media_id)
        message = oa_client.client.message.get_mass(self.msg_id)
        print message
        errcode = message['msg_status']
        raise UserError(_(message['msg_status']))


    def mass_send(self):
        def judge_content(content, openids):
            if len(openids)<2:
                raise UserError(_(u"群发用户对象至少是2两个！"))
            if content._name == 'wx.text':
                send_message=oa_client.client.message.send_mass_text(openids, content.text_content)
                errcode=send_message['errcode']
                if errcode==0:
                    self.state='2'
                    self.msg_id=send_message['msg_id']
                else:
                    raise UserError(_(send_message['errmsg']))
            elif content._name == 'wx.image':
                if content.media_id:
                    send_message=oa_client.client.message.send_mass_image(openids, content.media_id)
                    errcode = send_message['errcode']
                    if errcode == 0:
                        self.state = '2'
                        self.msg_id = send_message['msg_id']
                    else:
                        raise UserError(_(send_message['errmsg']))

                else:
                    raise UserError(_(u"media_id错误"))
            elif content._name == 'wx.imagetext' or content._name == 'wx.many.imagetext':
                send_message=oa_client.client.message.send_mass_article(openids, content.media_id)
                print send_message
                errcode = send_message['errcode']
                if errcode == 0:
                    self.state = '2'
                    self.msg_id = send_message['msg_id']
                else:
                    raise UserError(_(send_message['errmsg']))

        context = dict(self._context or {})
        active_ids = context.get('active_ids', [])[0]
        this = self.browse(active_ids)
        cr = self._cr
        wx_user =self.env['wx.user']
        query_tag = """
            SELECT DISTINCT
                a.openid
            FROM
            (
                SELECT DISTINCT
                    wx_user.nickname, wx_user.sex, wx_user.city,wx_user.country,wx_user.province, wx_user.openid
                FROM
                    public.wx_user,
                    public.wx_tag_wx_user_rel,
                    public.wx_mass_message_wx_tag_rel,
                    public.wx_mass_message,
                    public.wx_tag
                WHERE
                    (wx_mass_message.id = {mass_id} AND
                    wx_mass_message_wx_tag_rel.wx_mass_message_id = wx_mass_message.id AND
                    wx_mass_message_wx_tag_rel.wx_tag_id = wx_tag.id AND
                    wx_tag_wx_user_rel.wx_tag_id = wx_tag.id)
            ) as a
        """
        this.mass_sex = this.mass_sex or 3

        mass_id = context['active_ids'][0]
        openids = []
        if self.user_ids:
            for user_id in self.user_ids:
                openids.append(user_id.openid)
            print this.content
            judge_content(this.content, openids)

        else:
            if this.mass_tags:
                if this.city:
                    if this.mass_sex != 3:
                        query0 = query_tag + " WHERE a.sex = {sex} AND a.{addr_area} = '{addr}'"
                        query = query0.format(mass_id=mass_id, sex=this.mass_sex, addr_area='city', addr=this.city)
                        self.env.cr.execute(query)
                    else:
                        query0 = query_tag + " WHERE a.{addr_area} = '{addr}'"
                        query = query0.format(mass_id=mass_id, addr_area='city', addr=this.city)
                        self.env.cr.execute(query)
                elif this.province:
                    if this.mass_sex != 3:
                        query0 = query_tag + " WHERE a.sex = {sex} AND a.{addr_area} = '{addr}'"
                        query = query0.format(mass_id=mass_id, sex=this.mass_sex, addr_area='province', addr=this.province)
                        self.env.cr.execute(query)
                    else:
                        query0 = query_tag + " WHERE a.{addr_area} = '{addr}'"
                        query = query0.format(mass_id=mass_id, addr_area='province', addr=this.province)
                        self.env.cr.execute(query)
                elif this.country:
                    if this.mass_sex != 3:
                        query0 = query_tag + " WHERE a.sex = {sex} AND a.{addr_area} = '{addr}'"
                        query = query0.format(mass_id=mass_id, sex=this.mass_sex, addr_area='country', addr=this.country)
                        self.env.cr.execute(query)
                    else:
                        query0 = query_tag + " WHERE a.{addr_area} = '{addr}'"
                        query = query0.format(mass_id=mass_id, addr_area='country', addr=this.country)
                        self.env.cr.execute(query)
                else:
                    if this.mass_sex != 3:
                        query0 = query_tag + " WHERE a.sex = {sex}"
                        query = query0.format(mass_id=mass_id, sex=this.mass_sex)
                        self.env.cr.execute(query)
                    else:
                        query = query_tag.format(mass_id=mass_id)
                        self.env.cr.execute(query)
                openids = map(lambda x: x[0], self.env.cr.fetchall())

                judge_content(this.content, openids)
            else:
                if this.city:
                    if this.mass_sex != 3:
                        users = wx_user.search(
                            [('city', '=', this.city), ('sex', '=', this.mass_sex)])
                    else:
                        users = wx_user.search([('city', '=', this.city)])
                elif this.province:
                    if this.mass_sex != 3:
                        users = wx_user.search([('province', '=', this.province),('sex', '=', this.mass_sex)])
                    else:
                        users = wx_user.search([('province', '=', this.province)])
                elif this.country:
                    if this.mass_sex != 3:
                        users = wx_user.search([('country', '=', this.country),('sex', '=', this.mass_sex)])
                    else:
                        users = wx_user.search([('country', '=', this.country)])
                else:
                    if this.mass_sex != 3:
                        users = wx_user.search([('sex', '=', this.mass_sex)])
                    else:
                        users = wx_user.search([])
                for user in users:
                    openids.append(user.openid)
                judge_content(this.content, openids)