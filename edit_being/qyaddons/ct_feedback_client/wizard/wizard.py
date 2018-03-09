# -*- coding: utf-8 -*-
from odoo import api, models, fields, SUPERUSER_ID, _
from odoo.exceptions import UserError, ValidationError
from odoo.osv import osv

import xmlrpclib
import datetime


# CREDENTIALS OF THE USER USED BY THE REMOTE PLATFORM TO UPDATE STATUES OF FEEDBACKS
FEEDBACK_SERVER_USER_LOGIN = 'feedback_server_agent'
FEEDBACK_SERVER_USER_PASSWORD = 'feedback'


DEV_PLATFORM_URL_PARAM_TAG = 'cotong.qitongyun.dev_platform.url'
DEV_PLATFORM_DB_PARAM_TAG = 'cotong.qitongyun.dev_platform.db'


class FeedbackUserConfigWizard(models.TransientModel):
    '''
    WIZARD USED TO SETUP THE CREDENTIALS OF THE USER USED BY THE REMOTE PLATFORM TO UPDATE STATUES OF FEEDBACKS
    '''
    _name = 'ct_feedback_client.feedback_user_config.wizard'

    @api.model
    def setup_feedback_user(self):
        if self.env.uid != SUPERUSER_ID:
            return

        Users = self.env['res.users']
        ChangePasswordWizard = self.env['change.password.wizard']

        update_data = {'name': 'Feedback Agent', 'login': FEEDBACK_SERVER_USER_LOGIN}

        feedback_user = Users.search(
            [('login', '=', FEEDBACK_SERVER_USER_LOGIN), '|', ('active', '=', False), ('active', '=', True)], limit=1)
        if not feedback_user:
            update_data['groups_id'] = [(6, 0, [self.env.ref('ct_feedback_client.group_feedback_user').id])]
            feedback_user = Users.create(update_data)

        if feedback_user:
            wizard = ChangePasswordWizard.create({'user_ids': [(0, 0, {
                'user_id': feedback_user.id,
                'user_login': feedback_user.login,
                'new_passwd': FEEDBACK_SERVER_USER_PASSWORD,
            })]})
            wizard.with_context(feedback_config=True).change_password_button()
        return



# CREDENTIALS OF USER USED TO REPORT THE ISSUE IN THE DEV PLATFORM
FEEDBACK_USER_LOGIN = 'feedback_agent'
FEEDBACK_USER_PASSWORD = 'feedback'

class FeedbackSubmitWizard(models.TransientModel):
    '''
    WIZARD USED TO REPORT THE ISSUE IN THE DEV PLATFORM
    '''
    _name = "ct_feedback_client.feedback.submit.wizard"

    @api.model
    def get_server_config(self):
        return {
            'server_url': self.env['ir.config_parameter'].sudo().get_param(DEV_PLATFORM_URL_PARAM_TAG),
            'server_db': self.env['ir.config_parameter'].sudo().get_param(DEV_PLATFORM_DB_PARAM_TAG)
        }

    # 给企通云服务器提交一个问题
    @api.model
    def submit_feedback(self, title, email, description, feedback_url, feedback_submitter, submitter_database=None):
        # THE CLIENT PLATFORM USER FEEDBACK SERVER AGENT CREDENTIALS TO SUBMIT THE FEEDBACK(ISSUE) IN THE SERVER PLATFORM

        config = self.get_server_config()
        url = config["server_url"]
        db = config["server_db"]

        info = False
        if url and db:
            try:
                common = xmlrpclib.ServerProxy('{}/xmlrpc/2/common'.format(url))
                models = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(url))
                uid = common.authenticate(db, FEEDBACK_USER_LOGIN, FEEDBACK_USER_PASSWORD, {'raise_exception': True})

                if not uid:
                    # print '******LOGIN REJECTED******'
                    return False

                info_vals = {
                    'name': title,
                    'email': email,
                    'description': description,
                }

                info = self.env['ct_feedback_client.question'].create(info_vals)
                issue_vals = {
                    'info_num':info.info_num,
                    'name': info.name,
                    'submitter_email': email,
                    'description': description,
                    'submitter_db':submitter_database,
                    'submitter_name': feedback_submitter,
                    'submitter_host': feedback_url,
                    'issue_stage_id': False,
                    'is_feedback': True,
                    'user_id': False,
                    'im_chat_url': info.chat_url
                }
                id = models.execute_kw(db, uid, FEEDBACK_USER_PASSWORD, 'project.issue', 'create', [issue_vals])
                if id:
                    return True
                else:
                    # print '*****FAILDED IN CREATING*****'
                    info.sudo().unlink()
                    return False
            except Exception as e:
                print 'EXCEPTION ', e
                info and info.sudo().unlink()
                return False
        else:
            return False



