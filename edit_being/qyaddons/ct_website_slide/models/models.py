# -*- coding: utf-8 -*-
from odoo import models, fields, api
from PIL import Image
from urllib import urlencode
from urlparse import urlparse

import datetime
import io
import json
import re
import urllib2

from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.tools import image
from odoo.tools.translate import html_translate
from odoo.exceptions import Warning
from odoo.addons.website.models.website import slug

class Slide(models.Model):

    _inherit = "slide.slide"



    # def _get_embed_code(self):
    #     base_url = self.env['ir.config_parameter'].get_param('web.base.url')
    #     for record in self:
    #         if record.datas and (not record.document_id or record.slide_type in ['document', 'presentation']):
    #             record.embed_code = '<iframe src="%s/slides/embed/%s?page=1" allowFullScreen="true" height="%s" width="%s" frameborder="0"></iframe>' % (base_url, record.id, 315, 420)
    #         elif record.slide_type == 'video' and record.document_id:
    #             if not record.mime_type:
    #                 # embed youtube video
    #                 record.embed_code = '<iframe src="//www.youtube.com/embed/%s?theme=light" allowFullScreen="true" frameborder="0"></iframe>' % (record.document_id)
    #             else:
    #                 # embed google doc video
    #                 record.embed_code = '<embed src="https://video.google.com/get_player?ps=docs&partnerid=30&docid=%s" type="application/x-shockwave-flash"></embed>' % (record.document_id)
    #         else:
    #             record.embed_code = False




    def _get_embed_code(self):
        for record in self:
            record.embed_code=self.url

            record.embed_code = "<embed  src= '%s'" \
                                " allowFullScreen = 'true'  width = '480' height = '400' > </embed>" % (self.url)

            #直接播放  Video URL
            # record.embed_code = "<video id='my-video' class='video-js vjs-big-play-centered' controls='auto' width='640' height='264'  data-setup='{}'>" \
            #                     "<source src='http://vjs.zencdn.net/v/oceans.mp4' type='video/mp4'></video>"


            # # 优酷播放  Video URL
            # record.embed_code ="<embed  src = 'http://player.youku.com/player.php/sid/XMjg2MDgzMjEwOA==/v.swf'" \
            #                    " allowFullScreen = 'true'quality = 'high'  width = '480' height = '400' align = 'middle'" \
            #                    " allowScriptAccess = 'always'  type='application/x-shockwave-flash'> </embed>"

            # # 爱奇艺播放  Video URL
            # record.embed_code="<iframe src= 'http://open.iqiyi.com/developer/player_js/coopPlayerIndex.html?" \
            #                   "vid=77a4ba9809e102a2148796a15c4d964c&tvId=485218900&accessToken=2.f22860a2479ad60d8da7697274de9346&" \
            #                   "appKey=3955c3425820435e86d0f4cdfe56f5e7&appId=1368'" \
            #                   " frameborder ='0'  allowfullscreen='true'  width = '480' height = '400'/>"





        print record.embed_code



    video_url=fields.Char(string="视频地址")


    @api.model
    def search_url(self,id):
        print id
        res=self.env['slide.slide'].search([('id','=',id)])
        data={
            'url':res.url
        }
        print data
        return data


    @api.onchange('url')
    def on_change_url(self):
        self.ensure_one()
        # if self.url:
        #     self.video_url=self.url
        #     res = self._parse_document_url(self.url)
        #     if res.get('error'):
        #         raise Warning(_('Could not fetch data from url. Document or access right not available:\n%s') % res['error'])
        #     values = res['values']
        #     if not values.get('document_id'):
        #         raise Warning(_('Please enter valid Youtube or Google Doc URL'))
        #     for key, value in values.iteritems():
        #         setattr(self, key, value)





    @api.model
    def create(self, values):
        if not values.get('index_content'):
            values['index_content'] = values.get('description')
        if values.get('slide_type') == 'infographic' and not values.get('image'):
            values['image'] = values['datas']
        if values.get('website_published') and not values.get('date_published'):
            values['date_published'] = datetime.datetime.now()
        if values.get('url'):
            values['video_url']= self.url

        #     doc_data = self._parse_document_url(values['url']).get('values', dict())
        #     for key, value in doc_data.iteritems():
        #         values.setdefault(key, value)
        # Do not publish slide if user has not publisher rights
        if not self.user_has_groups('website.group_website_publisher'):
            values['website_published'] = False
        slide = super(Slide, self).create(values)
        slide.channel_id.message_subscribe_users()
        slide._post_publication()
        return slide



    @api.multi
    def write(self, values):
        if values.get('url'):
            if values.get('url'):
                values['video_url'] = self.url
        #     doc_data = self._parse_document_url(values['url']).get('values', dict())
        #     for key, value in doc_data.iteritems():
        #         values.setdefault(key, value)
        if values.get('channel_id'):
            custom_channels = self.env['slide.channel'].search([('custom_slide_id', '=', self.id), ('id', '!=', values.get('channel_id'))])
            custom_channels.write({'custom_slide_id': False})
        res = super(Slide, self).write(values)
        if values.get('website_published'):
            self.date_published = datetime.datetime.now()
            self._post_publication()
        return res





