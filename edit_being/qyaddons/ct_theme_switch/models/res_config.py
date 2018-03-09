# -*- coding: utf-'8' "-*-"
from odoo import models, fields, api,_



class thmeSettings(models.TransientModel):
    _inherit = 'base.config.settings'

    theme = fields.Selection([
        ('ct_theme_switch.theme_default','主题1'),('ct_theme_switch.theme_red','主题2')
    ],string="主题", default_model='base.config.settings' )



    def get_default_theme(self,cr):
        configs = self.env['base.config.settings'].search([])
        length = len(configs)
        if length != 0:
            config = configs[-1]
            return {"theme": config.theme}
        else:
            return {}



