# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo import SUPERUSER_ID

class feedback_config_settings(models.TransientModel):
    _inherit = 'res.config.settings'
    _name = 'feedback.config.settings'

    feedback_url = fields.Char(string="URL", required=True, default_model='feedback.config.settings')
    feedback_db = fields.Char(string="数据库", required=True, default_model='feedback.config.settings')
    feedback_username = fields.Char(string="用户名", required=True, default_model='feedback.config.settings')
    feedback_password = fields.Char(string="密码", required=True, default_model='feedback.config.settings')

    def get_default_feedback(self,cr):
       # configs = api.Environment(cr, SUPERUSER_ID, {})['feedback.config.settings'].search([('1','=','1')])
        configs=self.env['feedback.config.settings'].search([])
        length = len(configs)
        if length != 0:
            config = configs[-1]
            return {"feedback_url": config.feedback_url, "feedback_db": config.feedback_db, \
                    "feedback_username": config.feedback_username, "feedback_password": config.feedback_password}
        else:
            return {}
