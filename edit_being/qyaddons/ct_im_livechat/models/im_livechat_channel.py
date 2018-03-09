# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import random
import re
from datetime import datetime, timedelta

from odoo import api, fields, models, modules, tools


class ImLivechatChannel(models.Model):
    _inherit =  'im_livechat.channel'

    @api.model
    def get_mail_channel(self, livechat_channel_id, anonymous_name):
        users = self.sudo().browse(livechat_channel_id).get_available_users()
        if len(users) == 0:
            users=self.env['res.users'].sudo().search([('super_chat','=',True)],limit=1)
            if not users:
                return False
        user = random.choice(users)
        operator_partner_id = user.partner_id.id
        # partner to add to the mail.channel
        channel_partner_to_add = [(4, operator_partner_id)]
        if self.env.user and self.env.user.active:  # valid session user (not public)
            channel_partner_to_add.append((4, self.env.user.partner_id.id))
        # create the session, and add the link with the given channel
        mail_channel = self.env["mail.channel"].with_context(mail_create_nosubscribe=False).sudo().create({
            'channel_partner_ids': channel_partner_to_add,
            'livechat_channel_id': livechat_channel_id,
            'anonymous_name': anonymous_name,
            'channel_type': 'livechat',
            'name': ', '.join([anonymous_name, user.name]),
            'public': 'private',
            'email_send': False,
        })
        return mail_channel.sudo().with_context(im_livechat_operator_partner_id=operator_partner_id).channel_info()[0]

    @api.model
    def get_livechat_info(self, channel_id, username='Visitor'):
        info = {}
        info['available'] = 1
        info['server_url'] = self.env['ir.config_parameter'].get_param('web.base.url')
        if info['available']:
            info['options'] = self.sudo().get_channel_infos(channel_id)
            info['options']["default_username"] = username
        return info

    # @api.model
    # def get_livechat_info(self, channel_id, username='Visitor'):
    #     info=super(ImLivechatChannel,self).get_livechat_info(channel_id, username='Visitor')
    #     info['available'] = 1
    #     return info


class ResUsers(models.Model):
    """ Channel Rules
        Rules defining access to the channel (countries, and url matching). It also provide the 'auto pop'
        option to open automatically the conversation.
    """
    _inherit = 'res.users'

    super_chat=fields.Boolean(string="超级客服")
