# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, tools, SUPERUSER_ID, _

class res_users(models.Model):
    _inherit='res.users'

    def __init__(self, pool, cr):
        super(res_users, self).SELF_WRITEABLE_FIELDS.append('svn_account')
        super(res_users, self).SELF_READABLE_FIELDS.append('svn_account')
        super(res_users, self).SELF_WRITEABLE_FIELDS.append('svn_password')
        super(res_users, self).SELF_READABLE_FIELDS.append('svn_password')
        super(res_users, self).SELF_READABLE_FIELDS.append('is_svn_user')


    def preference_change_svn_credentials(self):
        return {
            'type':'ir.actions.act_window',
            'res_model':'res.users.svn.wizard',
            'view_mode':'form',
            'view_type':'form',
            'target':'new',
        }


    svn_account = fields.Char(string='SVN account', copy=False)
    svn_password = fields.Char(string='SVN password', copy=False)
    is_svn_user = fields.Boolean(string='Is SVN user', copy=False)


class ChangeSVNCredentials(models.TransientModel):
    _name = 'res.users.svn.wizard'

    current_user_password = fields.Char(string='Password', required=True, translate=True)
    svn_account = fields.Char(string='SVN account', required=True, translate=True, default=lambda self: self.env.user.svn_account)
    svn_password = fields.Char(string='SVN account password', required=True, translate=True)

    def change_svn_credentials(self):
        self.env['res.users'].sudo().check(self._cr.dbname, self._uid, self.current_user_password)
        self.env.user.sudo().write({
            'svn_account': self.svn_account,
            'svn_password': self.svn_password
        })
        return {
            'type': 'ir.actions.client',
            'tag': 'reload_context',
        }
