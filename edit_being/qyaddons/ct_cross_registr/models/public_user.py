# -*- coding: utf-8 -*-
import datetime

from odoo import api, models, fields


class PublicUser(models.Model):
    _name = 'public.user'

    user_database=fields.Char(string="账套")
    user_name=fields.Char(string="用户名")
    user_password=fields.Char(string="密码")
    user_tel=fields.Char(string="手机")
    user_openid=fields.Char(string="微信ID")


    def create_date(self,vals):
        res=self.create(vals)
        return  res

    def search_openid(self,vals):
        openid=vals['openeid']
        user_database = vals['user_database']
        user_name = vals['user_name']
        user_password = vals['user_password']
        data = {
            'user_database': vals['user_database'],
            'user_name': vals['user_name'],
            'user_password': vals['user_password'],
            'user_tel': vals['user_tel'],
        }

        data_openid=self.sudo().search([('openid','=',openid)])

        #先查询是否已绑定微信
        if data_openid:#已绑定微信
            data.update({
            'openid':data_openid.openid
            })
        else:#未绑定微信
            #查询是否在主服务器存在数据
            data_openid = self.sudo().search([
                ('user_database', '=', user_database),
                ('user_name', '=', user_name),
                ('user_password', '=', user_password)
            ])
            if data_openid:#已存在数据未绑定微信
                data_openid.openid=openid
                data.update({
                    'openid': data_openid.openid
                })
            else:#未存在数据未绑定微信
                data.update({
                    'openid': data_openid.openid
                })
                self.create_date(data)

        return data





