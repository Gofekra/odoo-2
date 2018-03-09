# -*- coding: utf-8 -*-
from odoo import api, models, fields, SUPERUSER_ID, _
from odoo.exceptions import UserError, ValidationError
from odoo.osv import osv

import xmlrpclib
import datetime




'''
THIS CREDENTIALS ARE THE CREDENTIALS OF THE USER CREATED IN THE DEV PLATFORM:
THIS USER IS REMOTELY USED TO ONLY CREATE ISSUE: HE CANNOT EDIT, NEITHER UPDATE
NOTE: IF YOU CHANGE THIS CREDENTIALS, MAKE SURE IT IS THE SAME IN THE CLIENT MODULE CODE, BECAUSE IT IS CODE DEFINED
'''
FEEDBACK_USER_LOGIN = 'feedback_agent'
FEEDBACK_USER_PASSWORD = 'feedback'



class FeedbackUserConfigWizard(models.TransientModel):
    """
    THIS WIZARD IS USED TO SETUP THE PASSWORD OF THE LOCAL FEEDBACK AGENT USER
    AND ASSIGN IM TO THE GROUP: FEEDBACK USER
    THIS GROUP GIVES THE RIGHT ONLY TO CREATE AN ISSUE, NOT EDIT NEITHER UPDATE;
    
    THE USER IS CREATED WITHOUT PASSWORD IN THE FILE data/data.xml; THIS WIZARD FINDS
    THE USER BY THE DEFINED LOGIN in FEEDBACK_USER_LOGIN (it should be same as the one defined in data/data.xml)
    AND THEN SET THE VALUE DEFINED IN FEEDBACK_USER_PASSWORD AS PASSWORD;
    IF THE USER AS NOT BEEN CREATED , 
    HE HIS CREATED WITH FEEDBACK_USER_LOGIN and FEEDBACK_USER_PASSWORD AND ASSIGNED TO THE GROUP "Feedback agent user"
    """
    _name = "ct_feedback_server.feedback_user_config.wizard"

    @api.model
    def setup_feedback_user(self):
        if self.env.uid != SUPERUSER_ID:
            return

        Users = self.env['res.users']
        ChangePasswordWizard = self.env['change.password.wizard']

        update_data = {'name':'Feedback Agent','login':FEEDBACK_USER_LOGIN}

        feedback_user = Users.search([('login','=',FEEDBACK_USER_LOGIN), '|',('active','=',False),('active','=',True)], limit=1)
        if not feedback_user:
            update_data['groups_id'] = [(6,0,[self.env.ref('ct_feedback_server.group_feedback_user').id])]
            feedback_user = Users.create(update_data)

        if feedback_user:
            wizard = ChangePasswordWizard.create({'user_ids': [(0, 0, {
                'user_id': feedback_user.id,
                'user_login': feedback_user.login,
                'new_passwd': FEEDBACK_USER_PASSWORD,
            })]})
            wizard.with_context(feedback_config =True).change_password_button()
        return


'''
WITH THE ASSUMPTION THAT A USER WITH THE FOLLOWING CREDENTIALS EXISTS IN THE CLIENTS PLATFORMS;
THIS CREDENTIALS ARE USED TO REMOTELY: UPDATE STATUES OF THE FEEDBACK POSTED BY THE CLIENT PLATFORM
NOTE: IF YOU CHANGE THIS CREDENTIALS, MAKE SURE IT IS THE SAME IN THE CLIENT MODULE CODE, BECAUSE IT IS CODE DEFINED
'''
FEEDBACK_SERVER_USER_LOGIN = 'feedback_server_agent'
FEEDBACK_SERVER_USER_PASSWORD = 'feedback'


class FeedbackNotificationWizard(models.TransientModel):
    '''
    IN THIS WIZARD, THE SERVER PLATFORM UPDATES THE FEEDBACK IN THE CLIENT PLATFORMS
    USING FEEDBACK_SERVER_USER_LOGIN and FEEDBACK_SERVER_USER_PASSWORD AS WELL AS THE
    REQUIRED PARAMETERS FOR IT. IT MEANS THAT A USER WITH THOSE CREDENTIALS EXISTS IN THE 
    CLIENT PLATFORM: AS SAID BEFORE, IF YOU CHANGE IT, MAKE SURE THEY ARE SAME IN THE CLIENT MODULE CODE
    '''
    _name = "ct_feedback_server.feedback.wizard"

    @api.model
    def notify_feedback_state_change(self, database, url, question_num, new_state, update_data={}):
        if new_state not in ['submitted','handled','solved']:
            return False
        # print url
        try:
            # if url.contains(':') :
            #     url = url.split(":")[0]

            common = xmlrpclib.ServerProxy('{}/xmlrpc/2/common'.format(url))
            models = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(url))
            uid = common.authenticate(database, FEEDBACK_SERVER_USER_LOGIN, FEEDBACK_SERVER_USER_PASSWORD, {'raise_exception': True})
            if not uid:
                return False

            ids = models.execute_kw(database, uid, FEEDBACK_SERVER_USER_PASSWORD,'ct_feedback_client.question', 'search',
                                  [[['info_num', '=', question_num]]], {'limit': 1})
            # print 'SEARCH results for ', question_num, ids
            if ids:
                vals = {
                    'state': new_state,
                }
                vals.update(update_data)
                # if new_state == 'solved':
                #     vals['']
                update_statue = models.execute_kw(database, uid, FEEDBACK_SERVER_USER_PASSWORD, 'ct_feedback_client.question', 'write', [[ids[0]], vals])
                # print update_statue
                return update_statue
        except Exception as e:
            print 'EXCEPTION ', e

        return False


class FeedbackManagementWizard(models.TransientModel):
    _name = 'ct_feedback_server.wizard.issue'
    _description = 'Feedback Management Wizard'

    # submitter_email = fields.Char(string='Submitter email', translated=True)
    # submitter_name = fields.Char(string='Submitter', translated=True)
    # submitter_db = fields.Char(string='Submitter database', translated=True)
    # submitter_host = fields.Char(string='Submitter\'s host', translated=True)
    # info_num = fields.Char(string='Feedback number', translated=True)
    #
    # @api.model
    # def report_issue(self, info_num, name, submitter_email, description, submitter_db,
    #           submitter_name, submitter_host, issue_stage_id):
    #
    #     print '======REPORT ISSUE====='
    #
    #     return self.env['project.issue'].sudo().create({
    #         'info_num': info_num,
    #         'name': name,
    #         'submitter_email': submitter_email,
    #         'description': description,
    #         'submitter_db': submitter_db,
    #         'submitter_name': submitter_name,
    #         'submitter_host': submitter_host,
    #         'issue_stage_id': issue_stage_id,
    #     })
    #
    # @api.model
    # def create(self, vals):
    #     print '======CREATE======'
    #     print vals
    #     res = super(IssueCreationWizard, self).create(vals)
    #     return res

    @api.multi
    def assign_button(self):
        data = {'discarded':False, 'user_id': self.user_id.id}
        if self.feedback_id.feedback_stage_id == self.env.ref('ct_feedback_server.feedback_stage_unsolved'):
            data['feedback_stage_id'] = self.env.ref('ct_feedback_server.feedback_stage_inprocess').id
            data['notify_feedback_state_change'] = 'handled'
        self.feedback_id.write(data)
        # return {'type':'ir.actions.act_window.close'}
        return {'type':'ir.actions.act_window.close'}

    @api.multi
    def fix_button(self):
        data = {}
        if self.feedback_id.feedback_stage_id == self.env.ref('ct_feedback_server.feedback_stage_inprocess'):
            data['discarded'] = False
            data['fixed'] = True
            data['fixed_by'] = self.user_id.id
            data['fix_description'] = self.fix_description
            data['fix_date'] = datetime.datetime.now()
            data['feedback_stage_id'] = self.env.ref('ct_feedback_server.feedback_stage_solved').id

            data['notify_feedback_state_change'] = 'solved'
            data['notify_feedback_data'] = {'result_info': self.fix_description, 'fix_date': data['fix_date']}
            self.feedback_id.write(data)
        return {'type':'ir.actions.act_window.close'}


    feedback_id = fields.Many2one('project.issue', string='Feedback', ondelete='set null', readonly=True, required=True, translated=True)
    feedback_description = fields.Html(string='Description', readonly=True, related='feedback_id.description', translated=True)
    user_id = fields.Many2one('res.users', string='User', required=True, translated=True)
    operation_type = fields.Selection([
        ('assign','Assignment'),
        ('fix','Fix'),
    ], string='Type')
    fix_description = fields.Html(string='Explanation', required=True, translated=True)
