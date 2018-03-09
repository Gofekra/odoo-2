# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.tools import html2plaintext
from odoo import tools, _
from odoo.exceptions import ValidationError
from odoo.modules.module import get_module_resource
import time
from datetime import *

class Member(models.Model):

    _name = 'ct.member'
    _inherit = ['mail.thread']
    _description = ""

    @api.model
    def _default_image(self):
        image_path = get_module_resource('ct_member', 'static/src/img', 'default_image.png')
        return tools.image_resize_image_big(open(image_path, 'rb').read().encode('base64'))

    @api.model
    def _get_member_age_fnc(self):
        birthday = self.birthday
        today = date.today()
        try:
            born = birthday.replace(year=today.year)
        except ValueError:
            born = birthday.replace(year=today.year, day=birthday.day - 1)
        if born > today:
            return today.year - birthday.year - 1
        else:
            return today.year - birthday.year


    active = fields.Boolean(u'有效',default=True)


    #基本信息
    # image: all image fields are base64 encoded and PIL-supported
    image = fields.Binary("Photo", default=_default_image, attachment=True,
                          help="limited to 1024x1024px.")
    name = fields.Char(string=u'姓名')
    nickname = fields.Char(string=u'昵称')
    code = fields.Char(string=u'卡号')
    register_time = fields.Datetime(string=u'注册时间')
    birthday = fields.Date(string=u'生日')
    age = fields.Integer(string=u'年龄')

    gender = fields.Selection([
        ('male', u'男'),
        ('female', u'女')
        ],string=u'性别'
    )
    email = fields.Char(string=u'邮箱')
    QQ = fields.Integer(string='QQ')
    mobile = fields.Integer(string=u'手机')
    phone = fields.Integer(string=u'电话')

    #积分
    point = fields.Float(string=u'积分')


    # 地理信息
    province = fields.Many2one('ct.province',u'省')
    city = fields.Many2one('ct.city', u'市')
    district = fields.Many2one('ct.district', u'县/区')
    street = fields.Char(u'街道')

    # RFM属性
    order_number = fields.Integer(u'总下单次数')
    order_amount = fields.Integer(u'总下单金额')
    rma_number = fields.Integer(u'总退货次数')
    rma_amount = fields.Integer(u'总退货金额')

    channel_id = fields.Many2one('ct.channel', string=u'渠道')
    shop_id = fields.Many2one('ct.shop',u'所属门店')
    tag_ids = fields.Many2many('member.tag', 'member_tags_rel', 'member_id', 'tag_id', string='标签')

    create_id = fields.Many2one('res.users', string='创建人', default=lambda self: self.env.uid)

    @api.onchange('birthday')
    def _get_member_age(self):
        birthday = self.birthday
        if birthday:
            today = date.today()
            try:
                born = birthday.replace(year=today.year)
            except ValueError:
                born = birthday.replace(year=today.year, day=birthday.day - 1)
            if born > today:
                return today.year - birthday.year - 1
            else:
                return today.year - birthday.year
