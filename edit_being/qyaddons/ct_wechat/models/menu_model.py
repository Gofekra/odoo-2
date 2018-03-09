# -*- coding: utf-8 -*-
from odoo import models, fields, api

from autoreply_model import REPLY_CONTENT
from ..rpc import oa_client


MENU_ACTION_OPTION = REPLY_CONTENT + [('wx.url.redirection','跳转网页')]


class WxUrlRedirection(models.Model):
    _name = 'wx.url.redirection'
    _description = u'跳转网页'

    name = fields.Char(u'名称', )
    url = fields.Char(u'链接地址', help='http开头，如：http://www.baidu.com')


class MenuItemBase(models.AbstractModel):

    _name = 'wx.menu.item.base'
    
    menu_id = fields.Many2one('wx.menu', string='所属微信菜单', required=True, ondelete='cascade')
    sequence = fields.Integer('Sequence', help="sequence")
    name = fields.Char('子菜单', )
    action = fields.Reference(string='动作', selection=MENU_ACTION_OPTION)

    _order = 'sequence'


class MenuItemLeft(models.Model):
    _name = 'wx.menu.item.left'
    _description = u'左菜单项'
    _inherit = 'wx.menu.item.base'


class MenuItemMiddle(models.Model):
    _name = 'wx.menu.item.middle'
    _description = u'中菜单项'
    _inherit = 'wx.menu.item.base'

   
class MenuItemRight(models.Model):
    _name = 'wx.menu.item.right'
    _description = u'右菜单项'
    _inherit = 'wx.menu.item.base'


class WxMenu(models.Model):
    
    _name = 'wx.menu'
    _description = u'微信菜单'
    
    name = fields.Char('名称', )
    left_ids = fields.One2many('wx.menu.item.left', 'menu_id', '左菜单')
    middle_ids = fields.One2many('wx.menu.item.middle', 'menu_id', '中菜单')
    right_ids = fields.One2many('wx.menu.item.right', 'menu_id', '右菜单')
    left = fields.Char('左菜单')
    left_action = fields.Reference(string='动作', selection=MENU_ACTION_OPTION)
    middle = fields.Char('中菜单')
    middle_action = fields.Reference(string='动作', selection=MENU_ACTION_OPTION)
    right = fields.Char('右菜单')
    right_action = fields.Reference(string='动作', selection=MENU_ACTION_OPTION)
    sequence = fields.Integer('Sequence', help="sequence")
    
    _order = 'sequence'
    
    def _get_menu_action(self, name, action):
        if action and action._name=='wx.url.redirection':
            m_dict = {
	          	'type': 'view',
	          	'name': name,
	          	'url': str(action.url)
	        }
        else:
            m_dict = {
				'type': 'click',
				'name': str(name),
				'key': action and action._name + '_' + str(action.id) or ',0'
			}
        return m_dict
    
    def _get_menu_item(self, name, action, childs):
        if childs:
            child_list = []
            for child in childs:
                child_dict = self._get_menu_action(child.name, child.action)
                child_list.append(child_dict)
            return {
				'name': name,
				'sub_button': child_list
			}
        else:
            return self._get_menu_action(name, action)

    def do_active(self):
        context = dict(self._context or {})
        active_ids = context.get('active_ids', [])
        for active_ids in  active_ids:
            self = self.browse(active_ids)
            buttons = []
            if self.left:
                buttons.append(self._get_menu_item(self.left, self.left_action, self.left_ids))
            if self.middle:
                buttons.append(self._get_menu_item(self.middle, self.middle_action, self.middle_ids))
            if self.right:
                buttons.append(self._get_menu_item(self.right, self.right_action, self.right_ids))
            menu_data =  {"button": buttons}

            print menu_data
            oa_client.client.menu.create(menu_data)
