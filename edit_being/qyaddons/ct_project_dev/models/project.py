# -*- coding: utf-8 -*-
from lxml import etree
from odoo import api, fields, models, tools, SUPERUSER_ID, _
from odoo.exceptions import UserError, ValidationError, AccessError
from odoo.tools.safe_eval import safe_eval
import ast


class TaskStage(models.Model):
    _inherit = 'project.task.type'

    is_initial = fields.Boolean(string='Initial stage', help='If a task can be initiated at this stage')
    doublon_allowed = fields.Boolean(string='Doubles allowed', help='If this stage can contain many tasks having the same technical name',
                                     translated=True, default=True)
    parent_stage = fields.Many2one('project.task.type', string='Precedent stage', translated=True)
    user_ids = fields.Many2many('res.users', string='Responsible users', translated=True)
    related_fields = fields.Many2many('ir.model.fields', string='Related fields', translated=True, domain=[('model_id.model','=','project.task')])


def get_setting_value(self, param):
    return self.env['ir.values'].sudo().get_default(
        'ct_project.config.settings', param)


class Task(models.Model):
    _inherit = 'project.task'

    @api.onchange('stage_id')
    def _onchange_stage(self):
        # print 'stage changed!!!'
        return {}

    @api.depends('stage_id')
    def _compute_transferable(self):
        print '***********compute transferable**********'
        transfer_stage = self.env['project.task.type'].search([('id','=',get_setting_value(self, 'ct_project_upload_stage'))], limit=1)
        for rec in self:
            if transfer_stage:
                rec.transferable = rec.stage_id and (rec.stage_id.id != transfer_stage.id and rec.stage_id.sequence <= transfer_stage.sequence) or False

    @api.depends('stage_id')
    def _compute_reversible(self):
        print '***********compute reversible**********'
        transfer_stage = self.env['project.task.type'].search(
            [('id','=', get_setting_value(self, 'ct_project_upload_stage'))], limit=1)
        for rec in self:
            if transfer_stage:
                print 'Transfer stage sq : ', transfer_stage.sequence
                print 'record stage sq: ', rec.stage_id.sequence
                rec.reversible = rec.stage_id and (rec.stage_id.sequence >= transfer_stage.sequence and rec.stage_id.sequence <= transfer_stage.sequence) or False

    @api.depends('transfer_ids')
    def _compute_last_transfer_revision(self):
        for rec in self:
            revs = rec.transfer_ids.mapped('revision')
            #print revs
            if len(revs)>=2:
                rec.last_transfer_revision = revs[1]
            elif len(revs):
                rec.last_transfer_revision = revs[0]
            else:
                rec.last_transfer_revision = False

    @api.depends('transfer_ids')
    def _compute_current_transfer_revision(self):
        for rec in self:
            revs = rec.transfer_ids.mapped('revision')
            #print revs
            if len(revs):
                rec.current_transfer_revision = revs[0]
            else:
                rec.current_transfer_revision = False

    def _compute_issue_count(self):
        Issues = self.env['project.issue']
        for rec in self:
            rec.issue_count = Issues.search_count([('task_id','=', rec.id)])

    default_description="第一部分：应用场景"+'<br/><br/>'+"" \
                        "第二部分：开发设计"+'<br/><br/>'+"" \
                        "第三部分：开发描述及界面设计"+'<br/>'+ ""\
                        "功能：" + '<br/>' + ""\
                        "1.菜单" + '<br/>' + "" \
                        "2.字段说明" + '<br/><br/>' + ""\
                        " 3.控制说明" + '<br/><br/>' + ""\
                        "4.权限说明" + '<br/><br/>' + ""


    task_user_ids = fields.Many2many('res.users', string='Team Member')
    testreq_ids = fields.One2many('test.requirement', 'task_id', string='Test Requirement')
    '''the users assigned to the task must be svn users'''
    # testcase_ids = fields.One2many('test.case', 'task_id', string='测试用例', domain=[('is_svn_user','=',True)])
    testcase_ids = fields.One2many('test.case', 'task_id', string='Test Case')
    module_id = fields.Many2one('ct_project_dev.module', string='Module', translate=True, domain=[('active','=',True)])
    technical_name = fields.Char(string='Technical name', related='module_id.technical_name', translate=True, readonly=True)
    transferable = fields.Boolean(compute='_compute_transferable', store=True)
    reversible = fields.Boolean(compute='_compute_reversible', store=True)
    transfer_ids = fields.One2many('ct_project_dev.transfer', 'task_id', string='Transfer details', translate=True, readonly=True)
    last_transfer_revision = fields.Integer(string='Last transfer revision', compute='_compute_last_transfer_revision', tranlated=True)
    current_transfer_revision = fields.Integer(string='Current transfer revision', compute='_compute_current_transfer_revision', tranlated=True)
    issue_count = fields.Integer(string='', compute='_compute_issue_count')
    analysis_description = fields.Html(string='Analysis Description', translate=True)
    development_description = fields.Html(string='Development description', translate=True)
    # prototyping_description = fields.Html(string='Prototyping description', translate=True)
    deployment_description = fields.Html(string='Deployment description', translate=True)
    cancellation_description = fields.Html(string='Cancellation description', translate=True)
    description = fields.Html(string='Description',default=default_description)



    @api.multi
    def action_run_cmd(self):
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'ct_project_dev.linux_cmd.wizard',
            'form_type': 'form',
            'view_mode': 'form',
            'view_id': self.env.ref('ct_project_dev.cmd_wizard_form_view').id,
            'target':'new',
        }

    @api.multi
    def action_task_issues(self):
        action = self.env.ref('project_issue.project_issue_categ_act0').read()[0]
        action['domain'] = [('task_id','=',self.id)]
        new_context = ast.literal_eval(action['context'].replace(" ","").replace("\n","").replace("active_id","''"))

        active_model = self.env.context.get('active_model')
        active_id = self.env.context.get('active_id')
        print active_model, active_id

        if active_id and active_model == 'project.project':
            new_context.update({
                'default_project_id': active_id,
                'default_task_id':self.id,
                'active_id':active_id,
                'active_ids':[active_id],
                'active_model':active_model,
            })
        else:
            new_context.update({
                'default_project_id':self.project_id and self.project_id.id or False,
                'default_task_id':self.id,
                'active_id':self.project_id and self.project_id.id or False,
                'active_ids':[self.project_id and self.project_id.id or False],
                'active_model':'project.project',
            })

        action['context'] = new_context
        return action

    @api.multi
    def transfer_module(self):
        # if not (self.env.uid in self.task_user_ids.mapped('id') and self.env.uid in self.project_id.svn_user_ids.mapped('id')):
        if self.env.uid not in self.project_id.svn_user_ids.mapped('id'):
            # raise UserError(_('Only SVN users assigned to the project "%s" and this task can update it to this stage.') %  self.project_id.name)
            raise AccessError(
                _('Only SVN users assigned to the project "%s" can update it to this stage.') % self.project_id.name)

        res = {
            'name': 'Module Transfer Wizard',
            'type': 'ir.actions.act_window',
            'res_model': 'ct_project_dev.svn_wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_task_id': self.id,
                'default_name': self.technical_name,
                'default_sender_svn_account': self.env.user.svn_account,
                'default_sender_svn_password': self.env.user.svn_password,
                'default_svn_repository': self.project_id.repository_url,
            },
        }
        if self.env.context.get('active_model') == 'project.project':
            res['context'].update({'active_project':self.env.context.get('active_id')})
        return res

    @api.multi
    def revert_module(self):
        # if not (self.env.uid in self.task_user_ids.mapped('id') and self.env.uid in self.project_id.svn_user_ids.mapped('id')):
        if self.env.uid not in self.project_id.svn_user_ids.mapped('id'):
            # raise UserError(_('Only SVN users assigned to the project "%s" and this task can update it to this stage.') %  self.project_id.name)
            raise AccessError(
                _('Only SVN users assigned to the project "%s" can update it to this stage.') % self.project_id.name)

        res = {
            'name': 'Module Transfer Revert Wizard',
            'type': 'ir.actions.act_window',
            'res_model': 'ct_project_dev.svn_wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_task_id': self.id,
                'default_name': self.technical_name,
                'default_sender_svn_account': self.env.user.svn_account,
                'default_sender_svn_password': self.env.user.svn_password,
                'default_svn_repository': self.project_id.repository_url,
                'default_state': 'revert',
                'default_version': bool(self.last_transfer_revision) and str(self.last_transfer_revision) or False,
                'current_stage': self.stage_id and self.stage_id.id or False
            },
        }
        if self.env.context.get('active_model') == 'project.project':
            res['context'].update({'active_project':self.env.context.get('active_id')})
        return res

    @api.constrains('stage_id')
    def _check_stage(self):
        ProjectTask = self.env['project.task']
        ProjectTaskType = self.env['project.task.type']
        sensitive_stage_ids = ProjectTaskType.search([('doublon_allowed','=',False)]).mapped('id')
        for record in self:
            if record.stage_id and record.stage_id.id in sensitive_stage_ids:
                search_domain = [('technical_name', '=', record.technical_name),('stage_id', '=', record.stage_id.id)]
                count = ProjectTask.search_count(search_domain)
                if count > 1:
                    raise ValidationError(
                        _("Impossible to have many tasks with the same technical name in the stage '%s'" % record.stage_id.name))


    # ------------------------------------------------
    # CRUD overrides
    # ------------------------------------------------

    @api.model
    def create(self, vals):

        #         if self.env.uid not in self.env.ref('project.group_project_manager').users.mapped('id'):
        #             raise UserError(_('Only Project managers can create tasks.'))

        print '====CREATING TASK============'
        #print vals
        if vals.get('stage_id'):
            search_domain = [('id', '=', vals['stage_id'])]
            stage = self.env['project.task.type'].search(search_domain, limit=1)
            if stage and not stage.is_initial:
                raise UserError(_('A task cannot be created at this stage.'))
        new_record = super(Task, self).create(vals)
        return new_record


    @api.multi
    def write(self, vals):
        TaskStage = self.env['project.task.type']
        Wizard = self.env['ct_project_dev.svn_wizard']

        '''
        Checking if the fields to be modified are related to some stages
        and if the user has the right to modify the fields related to the current stage:
        foreach stage:
            check if one of the fields to be modified related to the stage
            if related to the stage, check if the user is one of the allowed users to manage the stage
        '''
        for stage in self.project_id.type_ids:
            stage_related_fields = set(stage.mapped('related_fields.name'))
            stage_related_users = set(stage.mapped('user_ids.id'))
            if bool( len(stage_related_fields.intersection( set(vals.keys()) )) ) and (self.env.uid not in stage_related_users):
                raise AccessError(_(
                    'The current user is not authorized to perform this action. Make sure the user has access rights on the fields related to the stage "%s"') % stage.name)

        # # stage_related_fields = set(self.project_id.type_ids.mapped('related_fields.name'))
        # stage_related_fields = set(self.stage_id.mapped('related_fields.name'))
        # # stage_related_users = set(self.project_id.type_ids.mapped('user_ids.id'))
        # stage_related_users = set(self.stage_id.mapped('user_ids.id'))
        # if bool( len(stage_related_fields.intersection( set(vals.keys()) )) ) and (self.env.uid not in stage_related_users):
        #     raise AccessError(_(
        #         'The current user is not authorized to perform this action. Make sure the user has access rights on the fields related to the stage "%s"') % self.stage_id.name)

        if 'stage_id' in vals and self.env.context.get('from_ui', False):
            upload_stage = get_setting_value(self, 'ct_project_upload_stage')
            previous_stage = self.stage_id
            new_stage = TaskStage.search([('id','=',vals['stage_id'])], limit=1)
            if new_stage and new_stage.id == upload_stage:
                '''
                only the svn users assigned to the task and the project can move it to the upload stage
                '''
                # if self.env.uid in self.task_user_ids.mapped('id') and self.env.uid in self.project_id.svn_user_ids.mapped('id'):
                if self.env.uid not in self.project_id.svn_user_ids.mapped('id'):
                    raise AccessError(_(
                        'Only testers assigned to the project "%s" can update the task to this stage.') % self.project_id.name)


                print '''Calling the script through the wizard'''
                #if self.env.context.get('from_ui', False):
                    # record_vals = {
                    #     'name': self.technical_name,
                    #     'sender_svn_account': self.env.user.sudo().svn_account,
                    #     'sender_svn_password': self.env.user.sudo().svn_password,
                    #     'svn_repository': self.sudo().project_id.repository_url,
                    #     'reload': True,
                    # }
                wizard = Wizard.with_context(
                    default_name = self.technical_name,
                    default_sender_svn_account = self.env.user.sudo().svn_account,
                    default_sender_svn_password = self.env.user.sudo().svn_password,
                    default_svn_repository = self.sudo().project_id.repository_url,
                    default_task_id = self.id,
                    default_auto_install = True,
                ).create({'update_stage':False})
                wizard.execute_py_svn()
            elif (previous_stage and previous_stage.id == upload_stage) and (new_stage.sequence < previous_stage.sequence):
                print '''revert the module to the previous transfer revision'''
                # record_vals = {
                #     'name': self.technical_name,
                #     'sender_svn_account': self.env.user.svn_account,
                #     'sender_svn_password': self.env.user.svn_password,
                #     'svn_repository': self.project_id.repository_url,
                #     'version': self.last_transfer_revision,
                #     'state':'revert',
                #     'reload': True,
                # }
                # wizard = Wizard.with_context(
                #         default_name = self.technical_name,
                #         default_sender_svn_account = self.env.user.svn_account,
                #         default_sender_svn_password = self.env.user.svn_password,
                #         default_svn_repository = self.project_id.repository_url,
                #         current_stage = self.stage_id,
                #         default_task_id = self.id
                #     ).create({'state':'revert', 'update_stage':False})
                # wizard.execute_py_svn()
        result = super(Task, self).write(vals)
        return result

    def unlink(self):
        if self.env.uid not in self.env.ref('project.group_project_manager').users.mapped('id'):
            raise UserError(_('Only Project managers can delete tasks.'))
        return super(Task, self).unlink()


class TestRequirement(models.Model):
    _name = 'test.requirement'
    _description = 'Test Requirement'
    _order = 'sequence, id'

    task_id = fields.Many2one('project.task', string='Task', index=True)
    sequence = fields.Char(string='Req No.', translate=True, required=True, index=True)
    description = fields.Char(string='Req Description', translate=True, required=True)
    exe_step = fields.Char(string='Execute Step', translate=True, required=True)
    expect_result = fields.Char(string='Expect Result', translate=True, required=True)
    dev_user_id = fields.Many2one('res.users', string='Developer', default=lambda self: self.env.uid)
    dev_finish_date = fields.Datetime(string='Finish Time', default=fields.Datetime.now)


class TestCase(models.Model):
    _name = 'test.case'
    _description = 'Test Case'
    _order = 'sequence, id'

    task_id = fields.Many2one('project.task', string='Task', index=True)
    sequence = fields.Char(string='Req or Bug No.', translate=True, required=True, index=True)
    test_step = fields.Char(string='Test Step', translate=True, required=True)
    test_input = fields.Char(string='Test Input', translate=True, required=True)
    expect_result = fields.Char(string='Expect Result', translate=True, required=True)
    result = fields.Selection([('normal', 'Normal'), ('blocked', 'Blocked'), ('processing', 'Processing')],
                              default='normal',
                              string='Result', translate=True, required=True, index=True)
    test_user_id = fields.Many2one('res.users', string='Tester', default=lambda self: self.env.uid)
    test_finish_date = fields.Datetime(string='Finish Time', default=fields.Datetime.now)
    note = fields.Char(string='Note', translate=True)


class Project(models.Model):
    _inherit = 'project.project'

    @api.model
    def _get_issue_type_common(self):
        IssueStage = self.env['project.issue.stage']
        return IssueStage.search([('case_default', '=', 1)], limit=1)

    # svn_path = fields.Char(string='SVN path', translate=True)
    svn_user_ids = fields.Many2many(
        'res.users',
        'project_svnuser_rel',
        string='Testers',
        domain=[('is_svn_user', '=', True)])
    repository_id = fields.Many2one('ct_project_dev.repository', string='Repository')
    repository_url = fields.Char(string='SVN repository url', related='repository_id.url', readonly=True)
    issue_stage_ids = fields.Many2many(
        'project.issue.stage',
        'project_issue_stage_rel',
        'project_id',
        'issue_stage_id',
        string='Issue Stages',
        #default=_get_issue_type_common,
        tranlated=True
    )
    module_ids = fields.One2many('ct_project_dev.module', 'project_id', string='Projects', translate=True)



class Command(models.Model):
    _name = 'ct_project_dev.command'

    name = fields.Char('Name', translate=True)
    cmd_params = fields.Char('Command params', translate=True)
    type = fields.Selection(string='Command type', selection=[('simple','Simple'), ('with_parameter','With parameter')], translate=True)


class Module(models.Model):
    _name = 'ct_project_dev.module'

    name = fields.Char(string='Name', translate=True)
    technical_name = fields.Char(string='Technical name', translate=True)
    description = fields.Text(string='Description', translate=True)
    active = fields.Boolean(string='Active', default=True, translate=True)
    project_id = fields.Many2one('project.project', string='String', translate=True)
    python_dependences = fields.Char(string='Python dependences', translate=True)
	
class ModulePythonDependence(models.Model):
	_name = 'ct_project_dev.module_pydep'
	
	name = fields.Char(string='Name', translate=True)



class ProjectSVNRepository(models.Model):
    _name = 'ct_project_dev.repository'

    name = fields.Char(string='Name', translate=True)
    url = fields.Char(string='SVN Respository URL')
    description = fields.Text(string='Description', translate=True)



class TransferDetail(models.Model):
    _name = 'ct_project_dev.transfer'
    _description = 'Module transfer information'
    _order = 'date desc, revision desc'

    @api.depends('author')
    def _compute_author_user(self):
        for rec in self:
            ResUsers = self.env['res.users']
            search_domain = [('is_svn_user','=',True), ('svn_account','=',rec.author)]
            rec.author_user = ResUsers.search(search_domain, limit=1)

    task_id = fields.Many2one('project.task', string='Task', translate=True)
    user_id = fields.Many2one('res.users', string='Responsible',
                              help='User who did the transfer',translate=True, default=lambda self: self.env.uid)
    date = fields.Datetime(string='Transfer time', translate=True, default=fields.Datetime.now)
    log_date = fields.Datetime(string='Log date', translate=True)
    message = fields.Text(string='Log message', translate=True)
    revision = fields.Integer(string='Revision', translate=True)
    author = fields.Char(string='Revision author', translate=True)
    author_user = fields.Many2one('res.users', compute='_compute_author_user',
                                  string='Revison Author(User)', translate=True,
                                  help='Odoo user related to the author of the revision')
    operation_type = fields.Selection([('transfer','Transfer'),('revert','Revert')], string='Operation type',translate=True)
    tag = fields.Selection([('good', 'Good'), ('bad', 'Dad')], string='Tag')

