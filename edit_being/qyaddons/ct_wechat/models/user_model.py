# -*- coding: utf-8 -*-
import datetime

from odoo import api, models, fields
import json,urllib2,time
from ..rpc import oa_client

class WxUser(models.Model):
    _name = 'wx.user'
    _description = u'微信用户'

    city = fields.Char(u'城市',)
    province = fields.Char(u'省份',)
    country = fields.Char(u'国家',)
    nickname = fields.Char(u'昵称',)
    remark = fields.Char(u'备注')
    tag_ids = fields.Many2many(
        'wx.tag', id1='user_id', id2='tag_id', string='标签')
    openid = fields.Char(u'用户标识', help='普通用户的标识，对当前公众号唯一', readonly=True)
    sex = fields.Selection([(1, u'男'), (2, u'女')], string=u'性别',)
    subscribe = fields.Selection(
        [(1, '已关注'), (2, '已拉黑'), (3, '未关注')], string=u'关注状态', default=3, readonly=True)
    subscribe_time = fields.Datetime(u'关注时间', readonly=True)
    headimgurl = fields.Char(u'头像url', readonly=True)
    headimg = fields.Html(compute='_get_headimg', string=u'头像', readonly=True)


    _rec_name ="nickname"

    @api.one
    def _get_headimg(self):
        self.headimg = '<img src=%s width="100px" height="100px" />' % self.headimgurl


    #转化时间戳
    def str_time(self,strtime):
        strtime = time.localtime(strtime)
        datetime=time.strftime('%Y-%m-%d %H:%M:%S', strtime)
        return datetime


    def grant_token(self,fields):
        """
        获取 Access Token 。
        详情请参考 http://mp.weixin.qq.com/wiki/index.php?title=通用接口文档

        :return: 返回的 JSON 数据包
        """
        app=self.env['wx.config.settings'].get_default_wx_appid(fields)
        corpid = app['wx_appid']
        corpsecret = app['wx_AppSecret']
        gettoken_url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s' % (
        corpid, corpsecret)
        request = urllib2.Request(gettoken_url)
        get_data = urllib2.urlopen(request).read()
        sort_data = json.loads(get_data)
        access_token = sort_data['access_token']
        return access_token




    def search_wx_tages(self):
        # first tages create

        token=self.grant_token(fields=None)
        tag_url='https://api.weixin.qq.com/cgi-bin/tags/get?access_token=%s' % (token)
        request = urllib2.Request(tag_url)
        get_data = urllib2.urlopen(request).read()
        sort_data = json.loads(get_data)
        sort_data=sort_data['tags']
        for sort_data in sort_data:
            values={
                'tag_id':str(sort_data['id']),
                'name': sort_data['name'],
            }
            res=self.env['wx.tag'].search([('name','=',sort_data['name'])])
            if not res:
              res=self.env['wx.tag'].create(values)
        return res

    def search_wx_user(self):
        self.unlink()
        data=oa_client.client.user.get_followers(first_user_id=None)
        openid=data['data']['openid']
        for openid in openid:
            user_data = oa_client.client.user.get(openid)
            var_data={
                'subscribe':user_data['subscribe'],
                'openid': user_data['openid'],
                'nickname': user_data['nickname'],
                'sex': user_data['sex'],
                'city': user_data['city'],
                'country': user_data['country'],
                'province': user_data['province'],
                'headimgurl':user_data['headimgurl'],
                'subscribe_time': self.str_time(user_data['subscribe_time']),
                'remark': user_data['remark'],
            }
            res=self.search([('openid','=',openid)])
            if not res:
                user_id=self.create(var_data)
                if user_data['tagid_list']:
                    for tag_ids in user_data['tagid_list']:
                        res_tag = self.env['wx.tag'].search([('tag_id', '=', tag_ids)])
                        if not res_tag:
                            result=self.search_wx_tages()
                        user_id.tag_ids+=res_tag
            else:
                if user_data['tagid_list']:
                    for tag_ids in user_data['tagid_list']:
                        res_tag = self.env['wx.tag'].search([('tag_id', '=', tag_ids)])
                        if  res_tag:
                            res.tag_ids += res_tag

                res.write(var_data)







class WxTag(models.Model):
    _name = 'wx.tag'
    _description = u'标签'

    tag_id = fields.Char(string='标签编号')
    name = fields.Char('标签名称', required=True)
    description = fields.Text(string='标签描述')
    user_ids = fields.Many2many(
        'wx.user', id1='tag_id', id2='user_id', string='标签')
