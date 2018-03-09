# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError
import datetime
from dateutil.relativedelta import relativedelta
import odoo.addons.decimal_precision as dp
import urllib
import urllib2
from odoo.exceptions import UserError

from odoo import api, fields, models
from odoo.tools.safe_eval import safe_eval
from odoo import api, fields, models, tools, SUPERUSER_ID, _


class ResUsers(models.Model):
    _inherit = 'res.users'
    tel = fields.Char(string='手机号', required=True)

    # is_manager = fields.Boolean('管理员', default=True)

    @api.model
    def create(self, values):
        user = super(ResUsers, self).create(values)
        print values
        if values.has_key('password'):
            password = values['password']
        else:
            password = user['password']
        name = user['login']
        tel = user.tel
        # db_name = self.env['ir.config_parameter'].sudo().get_param('web.base.url').replace('http://', '')
        db_name = '002.dxb.qitongyun.cn'
        data = {
            'db_name': db_name,
            'name': name,
            'password': password,
            'mobile': tel,
        }
        base_url = self.env['ir.config_parameter'].sudo().get_param('saas_center_user')
        base_url = 'http://manage.dxb.qitongyun.cn/'
        url = base_url + 'web/center_user'
        post_request(url, data)
        return user


class Users(models.Model):
    _inherit = "res.users"

    @api.multi
    def unlink(self):
        if SUPERUSER_ID in self.ids:
            raise UserError(_(
                'You can not remove the admin user as it is used internally for resources created by Odoo (updates, module installation, ...)'))
        db = self._cr.dbname
        for id in self.ids:
            self.__uid_cache[db].pop(id, None)
        base_url = 'http://manage.dxb.qitongyun.cn/'
        url = base_url + "web/saas_delete_user"
        for user in self:
            data = {
                'name': user.login,
                'mobile': user.mobile
            }
            post_request(url, data)
        return super(Users, self).unlink()

    # 重新实现在首选项修改密码事件
    @api.model
    def change_password(self, old_passwd, new_passwd):
        self.check(self._cr.dbname, self._uid, old_passwd)
        if new_passwd:
            # use self.env.user here, because it has uid=SUPERUSER_ID
            base_url = 'http://manage.dxb.qitongyun.cn/'
            url = base_url + "web/saas_change_password"
            db_name = '002.dxb.qitongyun.cn'
            data = {
                'db_name': db_name,
                'name': self.env.user.login,
                'mobile': self.env.user.mobile,
                'password': new_passwd,
            }
            post_request(url, data)
            return self.env.user.write({'password': new_passwd})
        raise UserError(_("Setting empty passwords is not allowed for security reasons!"))


class ChangePasswordUser(models.TransientModel):
    _inherit = 'change.password.user'

    # 重新实现更改密码按钮事件
    @api.multi
    def change_password_button(self):
        print ('change')
        for line in self:
            line.user_id.write({'password': line.new_passwd})
            base_url = 'http://manage.dxb.qitongyun.cn/'
            url = base_url + "web/saas_change_password"
            db_name = '002.dxb.qitongyun.cn'
            data = {
                'db_name': db_name,
                'name': line.user_id['login'],
                'mobile': line.user_id['mobile'],
                'password': line.new_passwd,
            }
            post_request(url, data)
        self.write({'new_passwd': False})


def post_request(url, data):
    try:
        post_data = urllib.urlencode(data)
        request = urllib2.Request(url, post_data)
        response = urllib2.urlopen(request)
        print ('response', response)
    except Exception as error:
        print error
        pass
        # raise UserError(_('There is no invoicable line.'))
