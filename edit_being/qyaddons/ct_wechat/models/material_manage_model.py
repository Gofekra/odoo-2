# -*- coding: utf-8 -*-
import io
import os
import base64
import tempfile
import StringIO
import cStringIO
from PIL import Image as PILImage

from odoo.http import request
from odoo import models, api, fields
from odoo.tools import image_save_for_web
from odoo.exceptions import AccessError
from odoo.tools.translate import _
from ..rpc import oa_client
from odoo.exceptions import UserError, ValidationError

class Text(models.Model):
    _name = 'wx.text'

    name = fields.Char('名字')
    text_content = fields.Text('文字内容', required=True)


class ImageText(models.Model):
    _name = 'wx.imagetext'

    name = fields.Char('标题', required=True)
    thumb_media_id = fields.Char('图文消息的封面图片素材id',reltead="image_id.media_id",readonly=True)
    author = fields.Char('作者', required=True)
    image_id = fields.Many2one(
        'wx.image', string='图片', required=True, ondelete='cascade')
    digest = fields.Text('摘要', help='选填，如果不填写会默认抓取正文前54个字')
    show_cover_pic = fields.Boolean('是否显示封面图片', default=1)
    content = fields.Html('正文', required=True)
    content_source_url = fields.Char('点击图文消息跳转链接')
    media_id = fields.Char('media_id', readonly=True)

    def get_wx_reply(self):
        return [self.name, self.digest, self.image_id.url, self.content_source_url]

    @api.multi
    def unlink(self):
        for self in self:
            try:
                 oa_client.client.material.delete( self.media_id)
            except Exception:
                pass
        return super(ImageText, self).unlink()



    @api.model
    def create(self,values):
        thumb_media_id = self.env['wx.image'].sudo().search([('id', '=', values['image_id'])]).media_id
        articles=[]
        articles.append({
            'thumb_media_id': thumb_media_id,
            'title':values['name'],
            'content': values['content'],
            'author': values['author'],
            'content_source_url':values['content_source_url'] or '',
            'digest':values['digest'] or '',
            'show_cover_pic':1
        })
        try:
            imagejson = oa_client.client.material.add_articles( articles)
            values['media_id'] = imagejson['media_id']
        except Exception, e:
            raise e
        return super(ImageText, self).create(values)

    @api.multi
    def write(self,values):
        raise AccessError(u"不能修改")

    def get_media_id(self):
        return self.media_id


class ManyImageText(models.Model):
    _name = 'wx.many.imagetext'

    name = fields.Char('名称')
    media_id = fields.Char('media_id', readonly=True)
    many_image_text = fields.Many2many(
        'wx.imagetext', string='图文')

    def get_wx_reply(self):
        articles = [article.get_wx_reply() for article in self.article_ids]
        return articles



    @api.model
    def create(self,values):
        articles=[]
        for many_image in values.get('many_image_text'):
            for many in many_image[-1:][0]:
                imagetext = self.env['wx.imagetext'].sudo().search([('id', '=', many)])
                articles.append({
                    'thumb_media_id': imagetext.image_id.media_id,
                    'title':imagetext.name,
                    'content': imagetext.name,
                    'author':imagetext.author,
                    'content_source_url':imagetext.content_source_url or '',
                    'digest':imagetext.digest or '',
                    'show_cover_pic':1
                })
        try:
            imagejson = oa_client.client.material.add_articles( articles)
            values['media_id'] = imagejson['media_id']
        except Exception, e:
            raise e
        return super(ManyImageText, self).create(values)


    @api.multi
    def unlink(self):
        for self in self:
            try:
                oa_client.client.material.delete( self.media_id)
            except Exception:
                pass
        return super(ManyImageText, self).unlink()


    @api.multi
    def write(self,values):
        raise AccessError(u"不能修改")

    def get_media_id(self):
        return self.media_id




class Image(models.Model):
    _name = 'wx.image'

    name = fields.Char('名字', required=True)
    image = fields.Binary('图片', required=True)
    media_id = fields.Char('media_id', readonly=True)
    url = fields.Char('url', readonly=True)
    #

    @api.multi
    def unlink(self):
        for self in self:
            try:
              oa_client.client.material.delete( self.media_id)
            except Exception:
                pass
        return super(Image, self).unlink()


    @api.model
    def create(self,values):
        image_path = base64_to_img(values.get('image'))
        image = open(image_path, 'rb')
        try:
            imagejson = oa_client.client.material.add(
                'image', image)
            values['media_id'] = imagejson['media_id']
            values['url'] = imagejson['url']
        except Exception, e:
            raise e
        finally:
        	image.flush()
        	image.close()
        return super(Image, self).create(values)

    @api.multi
    def write(self,values):
        raise AccessError(u"不能修改")

    def get_media_id(self):
        return self.media_id


def base64_to_img(image_b64):
    """base64转换成图片
    """
    image_data = base64.b64decode(image_b64)
    image_path = os.path.join(os.path.dirname(__file__) + '/../static/src/img/a.png')
    image = open(image_path, 'wb')
    image.write(image_data)
    image.close()
    return image_path
