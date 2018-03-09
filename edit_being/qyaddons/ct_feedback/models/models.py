# -*- coding: utf-8 -*-
from odoo import api, models, fields, SUPERUSER_ID, exceptions
from odoo.osv import osv
import xmlrpclib


class Issue(models.Model):
    _inherit = 'project.issue'

    submitter_email = fields.Char(string='Submitter email', translated=True)
    submitter_name = fields.Char(string='Submitter', translated=True)
    submitter_db = fields.Char(string='Submitter database', translated=True)
    submitter_host = fields.Char(string='Submitter\'s host', translated=True)
    info_num = fields.Char(string='Feedback number', translated=True)

    '''
    CRUD OVERRIDE
    '''
    @api.model
    def create(self, vals):
        print '''
            CREATING ISSUE
        '''
        print vals
        res = super(Issue, self).create(vals)
        return res


class Submit(models.TransientModel):
    _name = "ex.submit"

    @api.model
    def create_feedback_user(self):
        Users = self.env['res.users']
        ChangePasswordWizard = self.env['change.password.wizard']

        update_data = {'name':'Feedback Agent','login':'feedback_agent'}


        feedback_user = Users.search([('login','=','feedback_agent'), '|',('active','=',False),('active','=',True)], limit=1)
        if not feedback_user:
            feedback_user = Users.create(update_data)

        print 'Feedback user ID ', feedback_user.id
        print 'Feedback user login ', feedback_user.login

        wizard = ChangePasswordWizard.create({'user_ids': [(0, 0, {
            'user_id': feedback_user.id,
            'user_login': feedback_user.login,
            'new_passwd': 'fdbc',
        })]})
        wizard.change_password_button()

        # default_user = self.env.ref('base.default_user')

        # feedback_user = self.env.ref('ct_feedback.feedback_user')
        #
        # Users.signup(update_data, token=None)
        #
        # # default_user.write({'active':True})
        # # default_user.groups_id |= self.env.ref('base.group_user')
        # #feedback_user = Users.create(update_data)
        # # feedback_user.on_change_login()
        # # feedback_user.onchange_state()
        # # feedback_user.onchange_parent_id()
        # wizard = ChangePasswordWizard.create({'user_ids': [(0, 0, {
        #     'user_id': feedback_user.id,
        #     'user_login': feedback_user.login,
        #     'new_passwd': 'fdbc',
        # })]})
        # wizard.change_password_button()

        # if not feedback_user:
        #     # feedback_user = default_user.copy(default=update_data)
        #     feedback_user = Users.create(update_data)
        #     wizard = ChangePasswordWizard.create({'user_ids': [(0, 0, {
        #         'user_id': feedback_user.id,
        #         'user_login': feedback_user.login,
        #         'new_passwd': 'fdbc',
        #     })]})
        #     wizard.change_password_button()
        #
        #     # feedback_user.toggle_active()
        #     # feedback_user.toggle_active()
        #     #default_user.write(update_data)
        #     #default_user.groups_id |= self.env.ref('base.group_user')
        # else:
        #     pass
        #     feedback_user.write(update_data)
        #     feedback_user.groups_id |= self.env.ref('base.group_user')
        return


    @api.model
    def get_server_config(self):
        #configs = api.Environment()["feedback.config.settings"].search([])
        configs = self.env['feedback.config.settings'].search([])
        length = len(configs)
        if length == 0:
            return {"error": 1}
        else:
            config = configs[-1]
            return {"error": 0, "server_url": config.feedback_url, "server_db": config.feedback_db,
                    "server_username": config.feedback_username, "server_password": config.feedback_password}

    # 给企通云服务器提交一个问题
    @api.model
    def submit_feedback(self, title, email, description, feedback_url, feedback_submitter, submitter_database=None):
        config = self.get_server_config()
        if config["error"] == 1:
            return False
        # 服务器url
        url = config["server_url"]
        # 数据库名字
        db = config["server_db"]
        # 登录odoo的用户名
        username = config["server_username"]
        # 用户密码
        password = config["server_password"]
        #user=self.env['res.users'].search([('login','=',feedback_submitter)])

        # print title, email, description, feedback_url, feedback_submitter, submitter_database
        if url or db or username or password:
            try:
                # print url
                common = xmlrpclib.ServerProxy('{}/xmlrpc/2/common'.format(url))
                models = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(url))
                # uid = common.authenticate(db, username, password, {})
                uid = common.authenticate(db, 'feedback_agent', 'fdbc', {'raise_exception': True})

                if not uid:
                    return False

                print 'LOGGED IN WITH UID : ', uid

                info_vals = {
                    'name': title,
                    'email': email,
                    'description': description,
                }
                # print info_vals
                info = self.env['question.info'].create(info_vals)
                print info.info_num

                # print 'Checking Access Rights'
                # print models.execute_kw(db, uid, password,
                #                   'project.issue', 'check_access_rights',
                #                   ['read'], {'raise_exception': True})

                print 'CREATING ISSUE'
                # id = models.execute_kw(db, uid, password, 'ct_feedback_server.wizard.issue', 'report_issue', {
                # id = models.execute_kw(db, uid, password, 'ct_feedback_server.wizard.issue', 'create', [{
                id = models.execute_kw(db, uid, password, 'project.issue', 'create', [{
                    'info_num':info.info_num,
                    'name': info.name,
                    'submitter_email': email,
                    'description': description,
                    'submitter_db':submitter_database,
                    'submitter_name': feedback_submitter,
                    'submitter_host': feedback_url,
                    #'issue_stage_id': False,
                }], {'raise_exception': True})

                print id

                if id:
                    return True
                else:
                    info.unlink()
                    return False
            except Exception as e:
                print 'EXCEPTION ', e
                return False
        else:
            return False

class question_info(models.Model):
    _name = 'question.info'

    info_num = fields.Char(string="问题单号")
    name = fields.Char(string='问题标题', translated=True)
    email = fields.Char(string="电子邮件")
    description = fields.Char(string="问题描述")
    check_jind = fields.Char(string="跟踪进度")
    result_info = fields.Html(string="处理结果", translated=True)
    state = fields.Selection([('submitted','Submitted'), ('handled','Handled')], string='Status', default='submitted', translated=True)

    @api.model
    def create(self, vals):

        if 'info_num' not in vals:
            vals['info_num'] = self.env['ir.sequence'].sudo().next_by_code('question.info')
            #print vals['info_num']
        return super(question_info, self).create(vals)


    @api.model
    def search_info(self):
        data = self.env['question.info'].search([])
        res = []
        for data in data:
            res.append({
                'info_num':data.info_num,
                'name': data.name,
                'email': data.email,
                'description': data.description,
                'check_jind': data.check_jind,
                'result_info': data.result_info,
            })
        return res







