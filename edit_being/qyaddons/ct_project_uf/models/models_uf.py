# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""
__author__="chianggq@163.com"
__mtime__ = '2017-02-07 10:42:51'
"""
import datetime
from odoo.http import request
from odoo import models, fields, api, _
from odoo.exceptions import UserError

import traceback
import time

# class ct_project_uf(models.Model):
#     _name = 'ct_project_uf.ct_project_uf'

#     name = fields.Char()
para_context = {}

def addminute(bdate, addminute):
    if bdate:
        bdate = time.strptime(bdate, "%Y-%m-%d %H:%M:%S")
        y, m, d, hour, min, sec = bdate[0:6]
        bdate = datetime.datetime(y, m, d, hour, min, sec) + datetime.timedelta(minutes=addminute)
        return str(bdate)[0:19]
    else:
        return time.strftime("%Y-%m-%d %H:%M:%S")

def setContext(env, context):
    sesspara_obj = env['session.para']
    sesspara_obj.set_context(env.user.id, context)

def getContext(env):
    sesspara_obj = env['session.para']
    return sesspara_obj.get_context(env.user.id)

def getContextVal(env, key):
    sesspara_obj = env['session.para']
    return sesspara_obj.get_contextval(env.user.id, key)

def fun_default_task(env, uid):
    print "fun_myyyyyyyyyyyydefault_task uid:", uid
    try:
        # mycontext = para_context[uid]
        # active_id = mycontext['active_id'][0]
        active_id = getContextVal(env, 'active_id')
        # print "myyyyyyyyyyyyyactive_id:", active_id
        task_obj = env['project.task']
        task = task_obj.search([('id', '=', active_id)])
        print "task:", task.id
        return task.id or False
    except Exception, e:
        traceback.print_exc()
        return False

# def fun_default_project(pool, cr, uid):
#     try:
#         mycontext = para_context[uid]
#         active_id = mycontext['active_id'][0]
#         task_obj = pool.get('project.task')
#         task = task_obj.browse(cr, uid, active_id)
#         # print "project_id:",task.project_id
#         return task.project_id.id or False
#     except:
#         return False

def fun_default_project(env, uid):
    try:
        # print "come uid:", uid
        # mycontext = para_context[uid]
        # active_id = mycontext['active_id'][0]
        active_id = getContextVal(env, 'active_id')
        # print "come active_id:", active_id
        task_obj = env['project.task']
        task = task_obj.search([('id', '=', active_id)])
        # print "come task:", task
        # print "project_id:", task.project_id
        return task.project_id.id or False
    except Exception, e:
        traceback.print_exc()
        return False

def fun_default_name(pool, cr, uid):
    try:
        mycontext = para_context[uid]
        active_id = mycontext['active_id'][0]
        task_obj = pool.get('project.task')
        task = task_obj.browse(cr, uid, active_id)
        # print "active_id:",active_id
        return u'阶段报告:' + task.name or None
        # return 'stage Report:'+task.name or None
    except:
        return False

def fun_formatTime(bdate):
    if bdate:
        bdate = time.strptime(bdate, "%Y-%m-%d %H:%M:%S")
        y, m, d, hour, min, sec = bdate[0:6]
        bdate = datetime.datetime(y, m, d, hour, min, sec) + datetime.timedelta(hours=-8)
        return str(bdate)
    else:
        return time.strptime("%Y-%m-%d %H:%M:%S")

class PrjResUsers(models.Model):
    _inherit = 'res.users'

    def __init__(self, pool, cr):
        """ Override of __init__ to add access rights.
            Access rights are disabled by default, but allowed
            on some specific fields defined in self.SELF_{READ/WRITE}ABLE_FIELDS.
        """
        init_res = super(PrjResUsers, self).__init__(pool, cr)
        prj_fields = [
            'is_prjmgr',
            'is_prjtask',
        ]
        # duplicate list to avoid modifying the original reference
        type(self).SELF_WRITEABLE_FIELDS = list(self.SELF_WRITEABLE_FIELDS)
        type(self).SELF_WRITEABLE_FIELDS.extend(prj_fields)
        # duplicate list to avoid modifying the original reference
        type(self).SELF_READABLE_FIELDS = list(self.SELF_READABLE_FIELDS)
        type(self).SELF_READABLE_FIELDS.extend(prj_fields)
        return init_res

    is_prjmgr = fields.Boolean(u"是否项目经理", default=False,
                               groups="base.group_user")
    is_prjtask = fields.Boolean(u"是否执行任务", default=False,
                                groups="base.group_user")

class MyHrExpense(models.Model):
    _inherit = ['hr.expense']
    prj_id = fields.Many2one('project.project', string=u"项目")
    prjtask_id = fields.Many2one('project.task', string=u"任务")
    prjlog_id = fields.Many2one('uf.log', string=u"工作日志")

class project(models.Model):
    _inherit = ['project.project']

    # def _get_visibility_selection(self, cr, uid, context=None):
    #     """ Override to add customer option. """
    #     selection = super(project, self)._get_visibility_selection(cr, uid, context=context)
    #     idx = [item[0] for item in selection].index('public')
    #     selection.insert((idx + 1), ('customer', u'客户实施项目'))
    #     return selection
    #     # return [('public', 'All Users'),
    #     #         ('portal', 'Portal Users and Employees'),
    #     #         ('employees', 'Employees Only'),
    #     #         ('followers', 'Followers Only')]

    date_contract = fields.Integer(u'合同人天')
    date_impl = fields.Integer(u'已用人天')
    curstate = fields.Selection([('plan', u'项目规划'),
                                 ('design', u'蓝图设计'),
                                 ('build', u'系统建设'),
                                 ('switch', u'上线切换'),
                                 ('support', u'持续支持'),
                                 ],
                                u'当前项目状态', default='plan', required=False, copy=False)

    curstage_id = fields.Many2one('project.task.type', string=u'当前项目状态',domain="[('project_ids', '=', id)]",copy=False)


    # @api.model
    # def _get_cur_stages(self):
    #     print "comddddddddddddddddddddddddddddddddddd:",self.type_ids
    #     for prj in self:
    #         print prj.type_ids
    #
    #     return [('draft', "New")]
    #
    # _cur_stages = lambda self: self._get_cur_stages()
    # cur_stage = fields.Selection(_cur_stages, string=u'当前阶段', index=True)

    privacy_visibility = fields.Selection([
        # ('customer', u'客户实施项目'),
        ('followers', _('On invitation only')),
        ('employees', _('Visible by all employees')),
        ('portal', _('Visible by following customers')),
    ],
        string='Privacy', required=True,
        default='followers',
        help="Holds visibility of the tasks or issues that belong to the current project:\n"
             "- On invitation only: Employees may only see the followed project, tasks or issues\n"
             "- Visible by all employees: Employees may see all project, tasks or issues\n"
             "- Visible by following customers: employees see everything;\n"
             "   if website is activated, portal users may see project, tasks or issues followed by\n"
             "   them or by someone of their company\n")

    # product_id = fields.Many2one('product.product', string='Product', readonly=True, states={'draft': [('readonly', False)], 'refused': [('readonly', False)]}, domain=[('can_be_expensed', '=', True)], required=True)
    user_id = fields.Many2one('res.users', string='Project Manager', default=lambda self: self.env.user,
                              domain=[('is_prjmgr', '=', True)])

    def _myget_visibility_selection(self, cr, uid, context=None):
        """ Override to add customer option. """
        selection = super(project, self)._get_visibility_selection(cr, uid, context=context)
        idx = [item[0] for item in selection].index('public')
        selection.insert((idx + 1), ('customer', u'客户实施项目'))
        return selection
        # return [('public', 'All Users'),
        #         ('portal', 'Portal Users and Employees'),
        #         ('employees', 'Employees Only'),
        #         ('followers', 'Followers Only')]

class project_task(models.Model):
    _inherit = "project.task"

    # def read(self, cr, uid, ids, fields_to_read=None, context=None, load='_classic_read'):
    #     if context is None: context = {}
    #     records = super(project_task, self).read(cr, uid, ids, fields_to_read, context=context, load=load)
    #     # print "records:",records
    #     mycontext = dict(context, active_id=ids)
    #     para_context[uid] = mycontext
    #     return records

    # @api.multi
    # def read(self, fields=None, load='_classic_read'):
    #     print "im come hereeee:",self.ids[0]
    #     setContext(self.env, dict(active_id=self.ids[0]))
    #     return super(project_task, self).read(fields=fields, load=load)

    @api.multi
    def do_log(self):
        print "active_idactive_idactive_idactive_id:", self.ids
        # mycontext = dict(active_id=self.ids)
        # uid = self.env.user.id
        # para_context[uid] = mycontext
        setContext(self.env, dict(active_id=self.ids[0]))
        return {
            'view_type': 'form',
            'view_mode': 'form,tree',
            'res_model': 'uf.log',
            # 'target': 'new',
            'views': [(False, 'form'), (False, 'tree')],
            'type': 'ir.actions.act_window',
        }

    # doc_source = fields.Reference(selection=_get_document_types, string='Source Document', required=True, help="User can choose the source document on which he wants to create documents")
    name = fields.Char(u'任务摘要', track_visibility='onchange', size=128, required=True, select=True, translate=True)
    project_newdoc = fields.Reference(selection=[('uf.soft', u'软件确认单'),
                                                 ('uf.rpt.milestone', u'里程碑报告'),
                                                 ('uf.rpt.stage', u'项目阶段报告')
                                                 ], string=u'实施文档')
    user_id = fields.Many2one('res.users',
                              string='Assigned to',
                              default=lambda self: self.env.uid,
                              domain=[('is_prjtask', '=', True)],
                              index=True, track_visibility='always')

    # _columns = {
    #     'name': fields.char('Task Summary', track_visibility='onchange', size=128, required=True, select=True,translate=True),
    #     'project_doc': fields.reference('Project Document',
    #                                     selection=[('implement.handover', 'Implement Handover Sheet'), (
    #                                         'implement.install', 'Installation Confirmation Sheet'), (
    #                                                    'impl.rptmilestone', u'里程碑报告'), (
    #                                                    'impl.rptstage', u'项目阶段报告')])
    # }
    _order = "name, priority desc, sequence, date_start, id"

class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

    def _get_default_project(self):
        print "come to _get_default_project_get_default_project"
        return fun_default_project(self.env, self._uid)

    def _get_default_task(self):
        task= fun_default_task(self.env, self._uid)
        #print "tasssssssssssssssskkkk:",task
        return task

    def _get_default_time(self):
        return fields.Datetime.context_timestamp(self, datetime.datetime.now())

    def _get_next_time(self):
        context = dict(self._context or {})
        # print "context:",context
        # print "self.id:",self.task_id
        # print "requestidddddd:",request.params
        # print "requestidddsessionddd:",request.session
        #print "query_string:",request.query_string
        # active_ids = context.get('active_ids')
        # print "active_idsactive_idsactive_ids:",active_ids
        # mytask=self._get_default_task()
        # print "mytask:",mytask
        # print "last:",request.session.get('_last_accline_id')
        # if mytask :
        #     lastline=self.search([('task_id','=',mytask)],limit=1)
        #     print "lastline:",lastline
        #     if lastline:
        #         return addminute(lastline.date,int(lastline.unit_amount*60))

        return fields.Datetime.now()

    #task_id = fields.Many2one('project.task', 'Task', default=_get_default_task)
    # project_id = fields.Many2one('project.project', 'Project', domain=[('allow_timesheets', '=', True)])

    log_id = fields.Many2one('uf.log', u'日志')
    time_start = fields.Datetime(u'开始时间', default=_get_default_time)
    time_end = fields.Datetime(u'结束时间', default=_get_default_time)
    #date = fields.Datetime('Date', required=True, index=True, default=fields.Datetime.now)
    date = fields.Datetime('Date', required=True, index=True, default=_get_next_time)
    # mydatetime= fields.Datetime(u'日期', required=False, index=True, default=fields.Datetime.now)

    @api.model
    def create(self, vals):
        # print "AccountAnalyticLinevals:", vals
        if vals.get('log_id'):
            log_id = self.env['uf.log'].browse(vals.get('log_id'))
            project = self.env['project.project'].browse(log_id.project_id.id)
            print "projectidddddddddddddd:", project
            vals['account_id'] = project.analytic_account_id.id

        # last=self.search([('task_id','=',vals.get('task_id'))],limit=1)
        # if last:
        #      begindate=addminute(last.date,int(last.unit_amount*60))
        #      vals['date']=begindate
        resline= super(AccountAnalyticLine, self).create(vals)
        return resline

    _defaults = {
        #'task_id': _get_default_task,
        'time_start': fun_formatTime(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))),
        'time_end': fun_formatTime(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))),
        # time.strftime('%Y-%m-%d %H:%M:%S'),
        # 'project_id':  _get_default_project,
    }

class UfHandover(models.Model):
    _name = 'uf.handover'

    # name = fields.Char(u'实施项目交接单', required=True)
    # name = fields.Char(u'客户名称', required=True,default=u"客户")
    name = fields.Many2one('res.partner', u'客户名称', store=True)
    industry = fields.Char(u'所属行业')
    is_old_customer = fields.Boolean(u'是否老用户')
    main_products = fields.Char(u'生产的主要产品')
    current_software = fields.Text(u'目前使用软件')
    software_fee = fields.Float(u'软件金额', digits=(16, 2))
    implement_fee = fields.Float(u'实施金额', digits=(16, 2))
    extra_fee = fields.Float(u'佣金金额', digits=(16, 2))
    project_cost = fields.Float(u'项目成本', digits=(16, 2))
    total_price = fields.Float(u'项目总金额', digits=(16, 2))
    commissions_fee = fields.Float(u'佣金金额', digits=(16, 2))
    prepaid_implement_fee = fields.Float(u'已收实施费', digits=(16, 2))
    allocate_fee = fields.Float(u'划拨金额', digits=(16, 2))
    allocated_fee = fields.Float(u'划拨金额', digits=(16, 2))
    implement_person_days = fields.Integer(u'实施人天')
    handsel_person_days = fields.Integer(u'开发费用')
    has_dev = fields.Boolean(u'是否有开发')
    dev_person_days = fields.Integer(u'开发人天')
    dev_fee = fields.Float(u'开发费用', digits=(16, 2))
    dev_evaluator_id = fields.Many2one('res.users', u'开发评估人')
    main_function = fields.Text(u'开发主要功能')
    module_version = fields.Char(u'版本')
    db_number = fields.Integer(u'帐套数')
    module_note = fields.Text(u'模块备注')
    opposition_side = fields.Char(u'反对项目人员')
    collision_side = fields.Char(u'抵触项目人员')
    suggested_manager_id = fields.Many2one('res.users', u'建议项目经理')
    other_risk = fields.Text(u'其他风险')
    has_skilled_operator = fields.Boolean(u'操作人员是否有使用软件的经验')
    requirement_desc = fields.Text(u'需求描述')
    payment_plan = fields.Text(u'收款计划')
    salesman_id = fields.Many2one('res.users', u'销售人员')
    presale_consultant_id = fields.Many2one('res.users', u'售前顾问')
    project_manager_id = fields.Many2one('res.users', u'项目经理')
    implement_manager_id = fields.Many2one('res.users', u'实施经理')
    # project_id = fields.Many2one('project.project', u'项目', select=True)
    project_id = fields.Many2one('project.project', u'项目', index=True)
    order_id = fields.Many2one('sale.order', u'销售订单', required=False)
    user_id = fields.Many2one('res.users', u'用户', required=True, default=lambda self: self.env.user)

    # _columns = {
    #        'name': fields.char('Handover Sheet Title', required=True),
    #        'is_old_customer': fields.boolean('Is Old Customer'),
    #        'main_products': fields.char('Main Products'),
    #        'current_software': fields.text('Current Software'),
    #        'software_fee': fields.float('Software Fee', digits=(16, 2)),
    #        'implement_fee': fields.float('Implement Fee', digits=(16, 2)),
    #        'extra_fee': fields.float('Extra Fee', digits=(16, 2)),
    #        'project_cost': fields.float('Project Cost', digits=(16, 2)),
    #        'total_price': fields.float('Total Price', digits=(16, 2)),
    #        'commissions_fee': fields.float('Commissions', digits=(16, 2)),
    #        'prepaid_implement_fee': fields.float('Prepaid Implement Fee', digits=(16, 2)),
    #        'allocate_fee': fields.float('Allocate Fee', digits=(16, 2)),
    #        'allocated_fee': fields.float('Allocated Fee', digits=(16, 2)),
    #        'implement_person_days': fields.integer('Implement Person Days'),
    #        'handsel_person_days': fields.integer('Handsel Person Days'),
    #        'has_dev': fields.boolean('Development Included'),
    #        'dev_person_days': fields.integer('Development Person Days'),
    #        'dev_fee': fields.float('Development Fee', digits=(16, 2)),
    #        'dev_evaluator_id': fields.many2one('res.users', 'Evaluator'),
    #        'main_function': fields.text('Main Function'),
    #        'module_version': fields.char('Module Version'),
    #        'db_number': fields.integer('Database Number'),
    #        'module_note': fields.text('Module Note'),
    #        'opposition_side': fields.char('Opposition Side'),
    #        'collision_side': fields.char('Collision Side'),
    #        'suggested_manager_id': fields.many2one('res.users', 'Suggested Manager'),
    #        'other_risk': fields.text('Other Risk'),
    #        'has_skilled_operator': fields.boolean('Has Skilled Operator'),
    #        'requirement_desc': fields.text('Requirement Description'),
    #        'payment_plan': fields.text('Payment Plan'),
    #        'salesman_id': fields.many2one('res.users', 'Salesman'),
    #        'presale_consultant_id': fields.many2one('res.users', 'Presale Consultant'),
    #        'project_manager_id': fields.many2one('res.users', 'Project Manager'),
    #        'implement_manager_id': fields.many2one('res.users', 'Implement Manager'),
    #        'project_id': fields.many2one('project.project',u'项目', select=True),
    #        'order_id': fields.many2one('sale.order', u'销售订单', required=False),
    #    }

class UfHandoverService(models.Model):
    _name = 'uf.handover.service'

    name = fields.Char('Description', required=True)
    # seq = fields.Char('Sequence', required=True, default=lambda self:
    # self.env['ir.sequence'].get('uf.handover.service') or '1000')
    is_done = fields.Boolean('Done?')
    active = fields.Boolean('Active?', default=True)
    user_id = fields.Many2one('res.users', 'User', required=True, default=lambda self: self.env.user)
    last_use = fields.Datetime('LastUse', default=time.strftime('%Y-%m-%d %H:%M:%S'))
    # line_ids = fields.One2many('uf.handover.service.line', 'tpl_id', 'Lines')
    state = fields.Selection([('draft', 'New'),
                              ('open', 'In Progress'),
                              ('close', 'Closed')],
                             'Status', required=True, copy=False)
    name = fields.Char('name', required=True)

    # @api.model
    # def create(self, vals):
    #     print "ufhandoverservicevals:", vals
    #     ufhandoverservice_id = super(UfHandoverService, self).create(vals)
    #     return ufhandoverservice_id

    @api.one
    def do_toggle_done(self):
        # self.is_done = not self.is_done
        return True

    @api.multi
    def do_clear_done(self):
        # done_recs = self.search([('is_done', '=', True)])
        # done_recs.write({'active': False})
        return True

    def call_js(self, cr, uid, ids, context=None):
        context = {}
        # context["key"]="value"
        print "call--js..."
        ret = {
            'type': 'ir.actions.client',
            'tag': 'mytest',
            # 'context': context,
        }
        return ret

    @api.multi
    def do_action(self):
        ifdo = True
        res_id = 0
        if True:
            return {
                'view_type': 'form',
                'view_mode': 'form,tree',
                'res_model': 'uf.handover',
                'res_id': res_id,
                'views': [(False, 'form'), (False, 'tree')],
                'type': 'ir.actions.act_window',
            }

        return True

    @api.multi
    def do_print(self, cr, uid, ids, context=None):
        assert len(ids) == 1, 'This option should only be used for a single id at a time'
        return self.pool['report'].get_action(cr, uid, ids, 'ct_project_uf.uf_handover_service_report', context=context)

    @api.multi
    def do_preview(self, context=None):
        # assert len(self.ids) == 1, 'This option should only be used for a single id at a time'
        return {
            'name': 'action_uf_handover_service_report',
            'type': 'ir.actions.act_url',
            'url': '/report/html/ct_project_uf.uf_handover_service_report/' + str(self.ids[0]),
            'target': 'new',
        }

class UfLog(models.Model):
    _name = 'uf.log'

    def _get_default_project(self):
        # print "come to _get_default_project_get_default_project"
        return fun_default_project(self.env, self._uid)

    def _get_default_task(self):
        return fun_default_task(self.env, self._uid)

    def _get_default_product(self):
        try:
            taxproid = self.env.ref("ct_project_uf.bus_travel")
            return taxproid.id
        except:
            return None

    def _get_default_name(self):
        # vals['name'] = self.env['ir.sequence'].next_by_code('sale.order') or 'New'
        try:
            myname = self.env['ir.sequence'].next_by_code('uf.log') or '1000'
            return myname
        except:
            return None

    # name = fields.Char(u'日志编码', required=True, default=lambda self:self.env['ir.sequence'].get('uf.log') or '1000')
    name = fields.Char(u'日志编码', required=True, default=_get_default_name)
    project_id = fields.Many2one('project.project', u'项目', default=_get_default_project, required=True)
    task_id = fields.Many2one('project.task', u'任务', default=_get_default_task)
    # project_task_work = fields.One2many('project.task.work', 'log_id', u'工作')
    timesheet_ids = fields.One2many('account.analytic.line', 'log_id', u'工作')
    user_id = fields.Many2one('res.users', u'顾问', required=True, default=lambda self: self.env.user)
    company_id = fields.Many2one('res.partner', u'公司')
    confirm_date = fields.Date(u'确认日期')
    note = fields.Text(u'备注')
    hasprint = fields.Boolean(u'已打印', default=False)
    state = fields.Selection([('draft', u'草稿'),
                              ('audit', u'已审核'),
                              ],
                             u'状态', default='draft', required=True, copy=False)

    product_id = fields.Many2one('product.product', string=u'费用类别', default=_get_default_product,
                                 domain=[('can_be_expensed', '=', True)])
    amount = fields.Float(string=u'金额', default=0.0)
    route_des = fields.Char(string=u'行程', default="公交")
    taxiamount = fields.Float(string=u'出租车', default=0.0)

    # _defaults = {
    #     'confirm_date': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),  # time.strftime('%Y-%m-%d %H:%M:%S'),
    #     'project_id': _get_default_project,
    #     'task_id': _get_default_task,
    # }

    # _columns = {
    #    'log_number': fields.char('Log Number'),
    #    'project_id': fields.many2one('project.project', 'Project'),
    #    'project_task_work': fields.one2many('project.task.work', 'log_id', 'Task Work'),
    #    'user_id': fields.many2one('res.users', 'Consultant', required=True),
    #    'company_id': fields.many2one('res.partner', 'Company'),
    #    'confirm_date': fields.date('Confirm Date'),
    #    'note': fields.text('Note')


    def _get_default_project(self, cr, uid, context=None):
        return fun_default_project(self.pool, cr, uid)

    # @api.model
    # def create(self, vals):
    #     print "loggggggggggvals:", vals
    #     log_id = super(UfLog, self).create(vals)
    #     return log_id

    @api.model
    def create(self, vals):
        print "loggggggggggvals:", vals
        route_des = vals['route_des']
        product_id = vals['product_id']
        amount = vals['amount']
        taxiamount = vals['taxiamount']
        if float(amount) > 0 and product_id:
            pass
        else:
            vals['route_des'] = ''
            vals['amount'] = None
        log_id = super(UfLog, self).create(vals)
        print "log_id:", log_id

        if float(amount) > 0 and product_id:
            emps = self.env['hr.employee'].search([('user_id', '=', self._uid)])
            employee_id = emps[0].id if len(emps) > 0 else 0
            expvals = {'employee_id': employee_id, 'name': route_des, 'reference': False,
                       'description': False, 'payment_mode': 'own_account',
                       'product_id': product_id, 'unit_amount': amount, 'date': time.strftime('%Y-%m-%d'),
                       'tax_ids': [], 'message_ids': False, 'quantity': 1}
            expense_obj = self.env['hr.expense']
            expvals['prjtask_id'] = vals['task_id']
            expvals['prj_id'] = vals['project_id']
            expvals['prjlog_id'] = log_id.id
            expense_obj.create(expvals)

        if float(taxiamount) > 0:
            taxproid = self.env.ref("ct_project_uf.tax_travel")
            emps = self.env['hr.employee'].search([('user_id', '=', self._uid)])
            employee_id = emps[0].id if len(emps) > 0 else 0
            expvals = {'employee_id': employee_id, 'name': "出租车", 'reference': False,
                       'description': False, 'payment_mode': 'own_account',
                       'product_id': taxproid.id, 'unit_amount': taxiamount, 'date': time.strftime('%Y-%m-%d'),
                       'tax_ids': [], 'message_ids': False, 'quantity': 1}
            expense_obj = self.env['hr.expense']
            expvals['prjtask_id'] = vals['task_id']
            expvals['prj_id'] = vals['project_id']
            expvals['prjlog_id'] = log_id.id
            expense_obj.create(expvals)

        # task_id = fields.Many2one('crm.task', string="Task", copy=False)
        # partner_id = fields.Many2one('res.partner', string=u'客户')
        # lead_id = fields.Many2one('crm.lead', string=u'商机')
        return log_id

    @api.multi
    def write(self, vals):
        print "wrtevalues:", vals
        # route_des = vals['route_des']
        # product_id = vals['product_id']
        # amount = vals['amount']
        # if float(amount) > 0 and product_id:
        #     pass
        # else:
        #     vals['route_des'] = ''
        #     vals['amount'] = None
        exp_obj = self.env['hr.expense']
        super(UfLog, self).write(vals)
        for log in self:
            # if values.has_key('expense_ids'):
            print "logggggggggghere:", log
            exps = exp_obj.search([('prj_id', '=', log.project_id.id), ('prjtask_id', '=', log.task_id.id)])
            print "exps:", exps
            # if len(exps) > 0:
            #     amount = log.amount
            #     product_id = log.product_id
            #     if float(amount) > 0 and product_id:
            #         expvals = {'product_id': product_id.id, 'unit_amount': amount, 'date': time.strftime('%Y-%m-%d'),
            #                    'quantity': 1}
            #         # expvals['prjtask_id'] = vals['task_id']
            #         # expvals['prj_id'] = vals['project_id']
            #         exps[0].write(expvals)
            #     # if float(taxiamount) > 0:
            #     #     taxproid=self.env.ref("ct_project_uf.tax_travel")
            #     #     expvals = {'product_id': taxproid.id, 'unit_amount': amount, 'date': time.strftime('%Y-%m-%d'),
            #     #                'quantity': 1}
            #     #     # expvals['prjtask_id'] = vals['task_id']
            #     #     # expvals['prj_id'] = vals['project_id']
            #     #     exps[0].write(expvals)
            # else:
            if len(exps) > 0:
                sqldel = """delete from hr_expense where sheet_id is null and prj_id=%s
                          and prjtask_id=%s and prjlog_id=%s
                """ % (log.project_id.id, log.task_id.id, log.id)
                print "sqldel:", sqldel
                self._cr.execute(sqldel)

            if True:
                amount = log.amount
                product_id = log.product_id
                route_des = log.route_des
                taxiamount = log.taxiamount
                if float(amount) > 0 and product_id:
                    emps = self.env['hr.employee'].search([('user_id', '=', self._uid)])
                    employee_id = emps[0].id if len(emps) > 0 else 0
                    expvals = {'employee_id': employee_id, 'name': route_des, 'reference': False,
                               'description': False, 'payment_mode': 'own_account',
                               'product_id': product_id.id, 'unit_amount': amount, 'date': time.strftime('%Y-%m-%d'),
                               'tax_ids': [], 'message_ids': False, 'quantity': 1}
                    # expvals['prjtask_id'] = vals['task_id']
                    # expvals['prj_id'] = vals['project_id']
                    expvals['prjtask_id'] = log.task_id.id
                    expvals['prj_id'] = log.project_id.id
                    expvals['prjlog_id'] = log.id
                    exp_obj.create(expvals)


                if float(taxiamount) > 0:
                    taxproid = self.env.ref("ct_project_uf.tax_travel")
                    emps = self.env['hr.employee'].search([('user_id', '=', self._uid)])
                    employee_id = emps[0].id if len(emps) > 0 else 0
                    expvals = {'employee_id': employee_id, 'name': "出租车", 'reference': False,
                               'description': False, 'payment_mode': 'own_account',
                               'product_id': taxproid.id, 'unit_amount': taxiamount, 'date': time.strftime('%Y-%m-%d'),
                               'tax_ids': [], 'message_ids': False, 'quantity': 1}
                    expense_obj = self.env['hr.expense']
                    expvals['prjtask_id'] = log.task_id.id
                    expvals['prj_id'] = log.project_id.id
                    expvals['prjlog_id'] = log.id
                    expense_obj.create(expvals)
            return True

    @api.multi
    def do_wizard(self):
        for obj in self:
            # print "obdddddddddddddj:", self.ids
            return {
                'name': u'工作向导',
                'width': 200,
                'size': 'medium',
                'type': 'ir.actions.act_window',
                'res_model': 'uf.work.wizard',
                'view_mode': 'form',
                'view_type': 'form',
                # 'res_id': self.id,
                # 'views': [(False, 'form')],
                'target': 'new',
                'context': dict(self.env.context, mykey=1, active_ids=self.ids, active_id=self.ids[0]),
                'myresult': 1,
            }
        return False

    @api.multi
    def do_expense(self):
        return {
            'name': u'费用',
            # 'width': 200,
            # 'size': 'medium',
            'type': 'ir.actions.act_window',
            'res_model': 'hr.expense',
            'view_mode': 'list',
            'view_type': 'list',
            # 'res_id': self.id,
            # 'views': [(False, 'form')],
            # 'target': 'new',
            'context': dict(self.env.context, mykey=1, active_ids=self.ids, active_id=self.ids[0]),
            'myresult': 1,
        }

    @api.multi
    def do_copy(self):
        # uflog_obj=self.env['uf.log']
        uflogprint_obj = self.env['uf.log.print']
        uflogline_obj = self.env['uf.log.line']
        for obj in self:
            print "obj:", obj
            # project_id = obj.project_id
            # user_id = obj.user_id
            # name = obj.name
            # print "project_id:", project_id
            # print "user_id:", user_id
            # print "name:", name
            # taskworks = obj.project_task_work
            taskworks = obj.timesheet_ids
            # print "taskworks:", taskworks
            task_id = None
            for work in taskworks:
                task_id = work.task_id
                break

            print "task_id:", task_id
            task_id = task_id.id if task_id else False
            printvals = {'note': obj.note, 'project_id': obj.project_id.id, 'user_id': obj.user_id.id, 'name': obj.name,
                         'task_id': task_id, 'log_id': obj.id,
                         'print_date': time.strftime('%Y-%m-%d'), 'leave': False, 'line_ids': [], 'arrive': False}

            uflogprint_id = uflogprint_obj.create(printvals)
            print "uflogprint_id:", uflogprint_id
            obj.write({"hasprint": True})

            for work in taskworks:
                task_id = work.task_id
                ufloglinevals = {'begin_date': work.time_start, 'user_id': obj.user_id.id, 'name': work.name,
                                 'end_date': work.time_end, 'print_id': uflogprint_id.id}
                print "ufloglinevals:", ufloglinevals
                uflogline_obj.create(ufloglinevals)

            return {
                'view_type': 'form',
                'view_mode': 'form,tree',
                'res_model': 'uf.log.print',
                'res_id': uflogprint_id.id,
                'views': [(False, 'form'), (False, 'tree')],
                'type': 'ir.actions.act_window',
            }

        return True

    @api.multi
    def do_show(self):
        uflogprint_obj = self.env['uf.log.print']
        for obj in self:
            print "obj:", obj
            uflogprint = uflogprint_obj.search([('log_id', '=', obj.id)])
            if len(uflogprint) > 0:
                uflogprint_id = uflogprint[0]
                return {
                    'view_type': 'form',
                    'view_mode': 'form,tree',
                    'res_model': 'uf.log.print',
                    'res_id': uflogprint_id.id,
                    'views': [(False, 'form'), (False, 'tree')],
                    'type': 'ir.actions.act_window',
                }

        return True

class UfLogPrint(models.Model):
    _name = 'uf.log.print'

    # @api.model
    # def create(self, vals):
    #     print "vals:", vals
    #     logprint_id = super(UfLogPrint, self).create(vals)
    #     return logprint_id

    @api.model
    def create(self, vals):
        print "vals:", vals
        uflogprint_id = super(UfLogPrint, self).create(vals)
        return uflogprint_id

    def do_print(self):
        assert len(self._ids) == 1, 'This option should only be used for a single id at a time'
        # return self.pool['report'].get_action(cr, uid, ids, 'ct_project_uf.uf_log_print_report', context=context)
        return self.env['report'].get_action(self, 'ct_project_uf.uf_log_print_report')

    @api.multi
    def do_preview(self):
        # assert len(self.ids) == 1, 'This option should only be used for a single id at a time'
        return {
            'name': 'action_urlrevenue',
            'type': 'ir.actions.act_url',
            'url': '/report/html/ct_project_uf.uf_log_print_report/' + str(self.ids[0]),
            'target': 'new',
        }

    # name = fields.Char(u'日志编码', required=True, default=lambda self:
    # self.env['ir.sequence'].get('uf.log') or '1000')
    def _get_default_name(self):
        # vals['name'] = self.env['ir.sequence'].next_by_code('sale.order') or 'New'
        try:
            myname = self.env['ir.sequence'].next_by_code('uf.log') or '1000'
            return myname
        except:
            return None

    # name = fields.Char(u'日志编码', required=True, default=lambda self:self.env['ir.sequence'].get('uf.log') or '1000')
    name = fields.Char(u'日志编码', required=True, default=_get_default_name)

    project_id = fields.Many2one('project.project', u'项目', required=True)
    task_id = fields.Many2one('project.task', u'任务')
    log_id = fields.Many2one('uf.log', u'工作日志')
    user_id = fields.Many2one('res.users', u'顾问', required=True, default=lambda self: self.env.user)
    company_id = fields.Many2one('res.partner', u'公司')
    print_date = fields.Date(u'打印日期')
    arrive = fields.Datetime(u'到达时间')
    leave = fields.Datetime(u'离开时间')
    note = fields.Text(u'备注')
    impldate = fields.Integer(u'本次人天', default=1)
    curdate = fields.Integer(u'当前人天')

    state = fields.Selection([('draft', u'草稿'),
                              ('audit', u'已审核'),
                              ],
                             u'状态', default='draft', required=True, copy=False)
    line_ids = fields.One2many('uf.log.line', 'print_id', u'日志明细')

class UfLogLine(models.Model):
    _name = 'uf.log.line'

    @api.model
    def create(self, vals):
        print "ufloglinevals:", vals
        uflogline_id = super(UfLogLine, self).create(vals)
        return uflogline_id

    name = fields.Char(u'工作内容', required=True)
    begin_date = fields.Datetime(u'开始时间')
    end_date = fields.Datetime(u'结束时间')
    print_id = fields.Many2one('uf.log.print', u'盖章工作日志', ondelete='cascade', required=True)
    # 'hours': fields.float('Time Spent')
    user_id = fields.Many2one('res.users', u'顾问', required=True, default=lambda self: self.env.user)

class UfSoftModule(models.Model):
    _name = 'uf.soft.module'

    soft_id = fields.Many2one('uf.soft', u'软件确认单')
    software_id = fields.Many2one('product.product', u'软件名称')
    name = fields.Char(u'模块')
    version = fields.Char(u'版本')
    license_number = fields.Integer(u'序列号')
    note = fields.Selection([('newpur', u'新购'),
                             ('upgrade', u'升级'),
                             ('newmodule', u'新模块'),
                             ], u'备注')

    # _columns = {
    #    'install_id': fields.many2one('implement.install', 'Install Confirmation'),
    #    'software_id': fields.many2one('product.product', 'Software Name'),
    #    'module': fields.char('Module'),
    #    'version': fields.char('Version'),
    #    'license_number': fields.integer('License No.'),
    #    'note': fields.selection(
    #        [('new pur', 'NEW PURCHARSE'), ('upgrade', 'UPGRADE'), ('new_module', 'NEW COMPONENT')], 'Note')

class UfSoft(models.Model):
    _name = 'uf.soft'

    # name = fields.Char(u'软件安装确认单', required=True)
    name = fields.Many2one('res.partner', store=True)
    contract_number = fields.Char(u'销售合同号')
    dongle_number = fields.Char(u'加密锁编号')
    install_software = fields.One2many('uf.soft.module', 'soft_id', 'Software Module')
    software_pur_date = fields.Date(u'购买日期')
    has_lans = fields.Boolean(u'局域网')
    lan_speed = fields.Selection([('10m', '10MB'), ('100m', '100MB'), ('1000m', '1000MB')], u'局域网速率')
    dept_covered = fields.Text(u'覆盖部门')
    has_internet = fields.Boolean(u'广域网')
    internet_speed = fields.Selection([('10m', '10MB'), ('100m', '100MB'), ('1000m', '1000MB')], u'广域网速率')
    area_covered = fields.Text(u'覆盖范围')
    server_type = fields.Char(u'服务器类型')
    server_number = fields.Integer(u'数量')
    server_configuration = fields.Text(u'配置情况')
    os_type = fields.Char(u'操作系统', default=u'Windows')
    os_version = fields.Char(u'版本', default=u'Server 2008 R2')
    os_pur_date = fields.Date(u'购买日期')
    os_path = fields.Char(u'安装路径')
    db_type = fields.Char(u'数据库类型', default=u'SQL SERVER')
    db_version = fields.Char(u'版本', default=u'2005')
    db_pur_date = fields.Date(u'购买日期')
    db_path = fields.Char(u'安装路径')
    db_licence = fields.Char(u'许可数')
    checker_id = fields.Many2one('res.users', u'检查人')
    check_date = fields.Date(u'检查日期')
    service_note = fields.Text(u'服务记录', default=u'服务器安装完成；加密盒注册完成')
    service_engineer_id = fields.Many2one('res.users', u'服务工程师')
    service_date = fields.Date(u'服务日期')
    is_successful = fields.Boolean(u'是否成功')
    customer_note = fields.Text(u'客户意见')
    customer_note_date = fields.Date(u'客户意见日期')
    extra_note = fields.Text(u'备注')

    #  _columns = {
    #     'name': fields.char('Installation Sheet Title', required=True),
    #     'contract_number': fields.char('Contract Number'),
    #     'dongle_number': fields.char('Dongle Number'),
    #     'install_software': fields.one2many('implement.install.software', 'install_id', 'Software Module'),
    #     'software_pur_date': fields.date('Software Purchase Date'),
    #     'has_lans': fields.boolean('Has Lans'),
    #     'lan_speed': fields.selection([('10m', '10MB'), ('100m', '100MB'), ('1000m', '1000MB')], 'Lan Speed'),
    #     'dept_covered': fields.text('Dept. Covered'),
    #     'has_internet': fields.boolean('Has Internet'),
    #     'internet_speed': fields.selection([('10m', '10MB'), ('100m', '100MB'), ('1000m', '1000MB')], 'Internet Speed'),
    #     'area_covered': fields.text('Area Covered'),
    #     'server_type': fields.char('Server Type'),
    #     'server_number': fields.integer('Server No.'),
    #     'server_configuration': fields.text('Server Configuration'),
    #     'os_type': fields.char('OS Type'),
    #     'os_version': fields.char('OS Version'),
    #     'os_pur_date': fields.date('OS Purchase Date'),
    #     'os_path': fields.char('OS Path'),
    #     'db_type': fields.char('Database Type'),
    #     'db_version': fields.char('Database Version'),
    #     'db_pur_date': fields.date('Database Purchase Date'),
    #     'db_path': fields.char('Database Path'),
    #     'checker_id': fields.many2one('res.users', 'Checker'),
    #     'check_date': fields.date('Check Date'),
    #     'service_note': fields.text('Service Note'),
    #     'service_engineer_id': fields.many2one('res.users', 'Service Engineer'),
    #     'service_date': fields.date('Service Date'),
    #     'is_successful': fields.boolean('Is Successful'),
    #     'customer_note': fields.text('Customer Note'),
    #     'customer_note_date': fields.date('Customer Note Date'),
    #     'extra_note': fields.text('Extra Note')
    # }
    user_id = fields.Many2one('res.users', u'用户', required=True, default=lambda self: self.env.user)

class UfDataStatic(models.Model):
    _name = 'uf.data.static'

    name = fields.Char(u'单位名称', required=True)
    usemodule = fields.Char(u'使用模块')
    switch_user = fields.Char(u'切换负责人')
    telphone = fields.Char(u'电话')
    op_password = fields.Boolean(u'操作员是否都已设置密码?')
    support_person = fields.Boolean(u'权限分配、主数据维护、参数配置的工作是否有专门人员维护?')
    right_allocated = fields.Boolean(u'系统期初单据和期初余额的录入权限是否已分配到相应用户?')

    dept_doc = fields.Boolean(u'部门档案设置是否正确?')
    person_doc = fields.Boolean(u'人员档案设置是否正确?')
    cusclass_doc = fields.Boolean(u'客户分类设置是否正确?')
    customer_doc = fields.Boolean(u'客户档案设置是否正确?')
    contact_doc = fields.Boolean(u'客户联系人档案设置是否正确?')
    supclass_doc = fields.Boolean(u'供应商分类设置是否正确?')
    supplier_doc = fields.Boolean(u'供应商档案设置是否正确?')
    supcontact_doc = fields.Boolean(u'供应商联系人档案设置是否正确?')
    warehouse_doc = fields.Boolean(u'仓库/货位档案设置是否正确?')
    inout_type = fields.Boolean(u'收发类别设置是否正确?')
    stock_class = fields.Boolean(u'存货分类设置是否正确?')
    uom = fields.Boolean(u'存货档案设置是否正确?')
    bom_doc = fields.Boolean(u'物料清单设置是否正确?')
    work_doc = fields.Boolean(u'标准工序设置是否正确?')
    route_doc = fields.Boolean(u'工艺路线设置是否正确?')
    purchase_type = fields.Boolean(u'采购类型设置是否正确?')
    sale_type = fields.Boolean(u'销售类型设置是否正确?')
    item_doc = fields.Boolean(u'自由项档案设置是否正确?')
    stock_item = fields.Boolean(u'存货自由项对照表设置是否正确?')
    supplier_contrast = fields.Boolean(u'供应商存货对照表设置是否正确?')
    stock_contrast = fields.Boolean(u'客户存货对照表设置是否正确?')
    account = fields.Boolean(u'会计科目设置设置是否正确?')
    std_ratio = fields.Boolean(u'标准费率设置是否正确?')
    bank_doc = fields.Boolean(u'银行档案设置是否正确?')
    check_user = fields.Many2one('res.users', u'检查人')
    check_date = fields.Datetime(u'结束时间', default=fields.Datetime.now())
    user_id = fields.Many2one('res.users', u'用户', required=True, default=lambda self: self.env.user)

class UfDataDynamic(models.Model):
    _name = 'uf.data.dynamic'

    name = fields.Char(u'数据种类', required=True)
    daynum = fields.Integer(u'整理时间(天)')
    priority = fields.Integer(u'顺序优先级')
    res_user = fields.Many2one('res.users', u'负责人')
    fin_date = fields.Datetime(u'完成时间', default=fields.Datetime.now())
    remark = fields.Char(u'备注')
    iffin = fields.Boolean(u'是否完成', default=False)
    user_id = fields.Many2one('res.users', u'用户', required=True, default=lambda self: self.env.user)

class UfRptMilestone(models.Model):
    _name = 'uf.rpt.milestone'

    name = fields.Char(u'报告名称')
    project_id = fields.Many2one('project.project', u'项目')
    task_id = fields.Many2one('project.task', u'任务')
    user_id = fields.Many2one('res.users', u'顾问', required=True)
    company_id = fields.Many2one('res.partner', u'公司')
    rpt_date = fields.Date(u'报告日前')
    ifaudit = fields.Boolean(u'是否已审核?', default=False)
    note = fields.Text(u'备注')

class UfRptStage(models.Model):
    _name = 'uf.rpt.stage'

    #     "id","name","sequence","case_default","description"
    # "__export__.project_task_type_15","蓝图设计","1","True",""
    # "__export__.project_task_type_17","上线切换","1","True",""
    # "__export__.project_task_type_18","持续支持","1","True",""
    # "__export__.project_task_type_14","项目规划","1","True",""
    # "__export__.project_task_type_16","系统建设","1","True",""
    # "project.project_tt_analysis","分析","20","True",""
    # "project.project_tt_specification","规格","30","True",""

    def doaudit(self, cr, uid, ids, context=None):
        print "ids:", ids
        rptstage_obj = self.pool.get('uf.rpt.stage')
        project_obj = self.pool.get('project.project')
        # task_obj = self.pool.get('project.task')
        # type_obj = self.pool.get('project.task.type')
        rptstage = rptstage_obj.browse(cr, uid, ids)
        print "rptstage:", rptstage
        # #typeid=task_obj.browse( cr, uid, rptstage.task_id)#
        # typeid=rptstage.task_id
        # print "typeid:",typeid
        # print "typeid type:",type(typeid)
        # mystage=typeid.stage_id
        # print "mystage:",mystage.id
        mystageid = rptstage.task_id.stage_id.id
        myproid = rptstage.task_id.project_id.id
        # print "mystageid:", mystageid
        # print "myproid:", myproid
        prjobj = project_obj.browse(cr, uid, myproid)
        print "prjobj:", prjobj
        typestate = {'14': 'plan', '15': 'design', '15': 'build', '17': 'switch', '18': 'support'}
        cstatstr = typestate[str(mystageid)]
        # print "cstatstr:",cstatstr
        vals = {'cur_stage': mystageid, 'curstate': cstatstr, 'ifaudit': True}
        prjobj.write(vals)
        rptstage.write({'ifaudit': True})

        return True

    def _get_default_company(self, cr, uid, context=None):
        mycontext = para_context[uid]
        company_id = self.pool.get('res.users')._get_company(cr, uid, context=context)
        # if not company_id:
        # raise osv.except_osv(_('Error!'), _('There is no default company for the current user!'))
        return company_id

    def _get_default_task(self, cr, uid, context=None):
        mycontext = para_context[uid]
        active_id = mycontext['active_id'][0]
        return active_id or False

    def _get_default_project(self, cr, uid, context=None):
        mycontext = para_context[uid]
        active_id = mycontext['active_id'][0]
        task_obj = self.pool.get('project.task')
        task = task_obj.browse(cr, uid, active_id)
        # print "project_id:",task.project_id
        return task.project_id.id or False

    def _get_default_name(self, cr, uid, context=None):
        mycontext = para_context[uid]
        active_id = mycontext['active_id'][0]
        task_obj = self.pool.get('project.task')
        task = task_obj.browse(cr, uid, active_id)
        # print "active_id:",active_id
        return u'阶段报告:' + task.name or None
        # return 'stage Report:'+task.name or None

    name = fields.Char(u'报告名称')
    project_id = fields.Many2one('project.project', u'项目')
    task_id = fields.Many2one('project.task', u'任务')
    user_id = fields.Many2one('res.users', u'顾问', required=True)
    company_id = fields.Many2one('res.partner', u'公司')
    rpt_date = fields.Date(u'报告日前')
    ifaudit = fields.Boolean(u'是否已审核?', default=False)
    note = fields.Text(u'备注')

    _defaults = {
        'rpt_date': fields.Datetime.now,
        'company_id': _get_default_company,
        'task_id': _get_default_task,
        'project_id': _get_default_project,
        'name': _get_default_name,
        'user_id': lambda obj, cr, uid, context: uid,
        # 'name': lambda obj, cr, uid, context: '/',
    }

class UfWorkTpl(models.Model):
    _name = 'uf.work.tpl'

    name = fields.Char('模板名称', required=True)
    user_id = fields.Many2one('res.users', u'用户', required=True, default=lambda self: self.env.user)
    num = fields.Integer(u'使用次数', default=0)
    last_use = fields.Date(u'最近使用', default=time.strftime('%Y-%m-%d %H:%M:%S'))
    line_ids = fields.One2many('uf.work.line', 'tpl_id', u'模板明细')

    # @api.model
    # def create(self, vals):
    #     print "ufworktplvals:", vals
    #     ufworktpl_id = super(UfWorkTpl, self).create(vals)
    #     return ufworktpl_id

    @api.one
    def do_toggle_done(self):
        # self.is_done = not self.is_done
        return True

    @api.multi
    def do_clear_done(self):
        # done_recs = self.search([('is_done', '=', True)])
        # done_recs.write({'active': False})
        return True

    def call_js(self, cr, uid, ids, context=None):
        context = {}
        # context["key"]="value"
        print "call--js..."
        ret = {
            'type': 'ir.actions.client',
            'tag': 'mytest',
            # 'context': context,
        }
        return ret

    def do_print(self, cr, uid, ids, context=None):
        assert len(ids) == 1, 'This option should only be used for a single id at a time'
        return self.pool['report'].get_action(cr, uid, ids, 'cotong_project_uf.uf_work_tpl_report', context=context)

    @api.multi
    def do_preview(self, context=None):
        # assert len(self.ids) == 1, 'This option should only be used for a single id at a time'
        return {
            'name': 'action_uf_work_tpl_report',
            'type': 'ir.actions.act_url',
            'url': '/report/html/cotong_project_uf.uf_work_tpl_report/' + str(self.ids[0]),
            'target': 'new',
        }

class UfWorkLine(models.Model):
    _name = 'uf.work.line'

    name = fields.Char(u'工作描述', required=True)
    user_id = fields.Many2one('res.users', u'用户', required=True, default=lambda self: self.env.user)
    quantity = fields.Float('时间', default=1)
    tpl_id = fields.Many2one('uf.work.tpl', u'模板')
    hour_id = fields.Many2one('uf.work.hour', u'单位', default=1)

    # @api.model
    # def create(self, vals):
    #     print "ufworklinevals:", vals
    #     ufworkline_id = super(UfWorkLine, self).create(vals)
    #     return ufworkline_id

    @api.one
    def do_toggle_done(self):
        # self.is_done = not self.is_done
        return True

    @api.multi
    def do_clear_done(self):
        # done_recs = self.search([('is_done', '=', True)])
        # done_recs.write({'active': False})
        return True

    def call_js(self, cr, uid, ids, context=None):
        context = {}
        # context["key"]="value"
        print "call--js..."
        ret = {
            'type': 'ir.actions.client',
            'tag': 'mytest',
            # 'context': context,
        }
        return ret

    def do_print(self, cr, uid, ids, context=None):
        assert len(ids) == 1, 'This option should only be used for a single id at a time'
        return self.pool['report'].get_action(cr, uid, ids, 'cotong_project_uf.uf_work_line_report', context=context)

    @api.multi
    def do_preview(self, context=None):
        # assert len(self.ids) == 1, 'This option should only be used for a single id at a time'
        return {
            'name': 'action_uf_work_line_report',
            'type': 'ir.actions.act_url',
            'url': '/report/html/cotong_project_uf.uf_work_line_report/' + str(self.ids[0]),
            'target': 'new',
        }

class UfWorkHour(models.Model):
    _name = 'uf.work.hour'

    name = fields.Char(u'时间单位', required=True)
    coeficient = fields.Integer(u'换算系数', default=60)

class UfWorkWizard(models.TransientModel):
    _name = 'uf.work.wizard'
    _rec_name = 'begin_time'

    @api.multi
    def do_action(self):
        print "wwwwwwwwwwwwwwzid:", self.env.context
        active_id = self.env.context['active_id']
        log_obj = self.env['uf.log']
        # work_obj = self.env['project.task.work']
        work_obj = self.env['account.analytic.line']
        # worktpl_obj=self.env['uf.work.tpl']
        workhour_obj = self.env['uf.work.hour']
        workline_obj = self.env['uf.work.line']
        log = log_obj.browse(active_id)
        print "work:", log
        print "work log.task_id:", log.task_id
        print "work log.id:", log.id
        for wizard in self:
            print "wizard.tpl_id:", wizard.tpl_id
            print "wizard.opmode:", wizard.opmode
            print "begin_time:", wizard.begin_time
            # workvals = {'time_start': '2016-12-23 12:36:07', 'name': 'aaaa', 'task_id': 27, 'log_id': 29,
            #             'is_done': False, 'hours': 5, 'date': '2016-12-23 20:36:43', 'user_id': 1,
            #             'hr_analytic_timesheet_id': 21}
            # workvals = {'time_start': '2016-12-23 12:36:07', 'name': 'aaaa', 'task_id': log.task_id, 'log_id': log.id,
            #             'is_done': False, 'hours': 5, 'date': '2016-12-23 20:36:43', 'user_id': self.env.user.id}
            # AccountAnalyticLinevals = {u'user_id': 1, u'name': u'des1', u'task_id': 51, 'log_id': 37,
            #                            u'time_end': u'2017-02-20 01:36:36', u'unit_amount': 5,
            #                            u'time_start': u'2017-02-20 01:36:36'}
            print "111111111111111111:"
            tpl_lines = wizard.tpl_id.line_ids
            print "222222222222222222:"
            # tpl_lines=workline_obj.search([('tpl_id','=',wizard.tpl_id.id)],order='id desc')
            # print "tpl_linestpl_lines:",tpl_lines
            # todo:update num and last_date
            endtime = addminute(wizard.begin_time, 210)
            print "endtimeeeeeeeeeeeeee:", endtime
            print "myhour:", 210 / 60
            myhour = 210 / 60
            fmyhour = '%.2f' % myhour
            print "fmyhour:", fmyhour
            print "tpl_lines:", tpl_lines
            time_start = wizard.begin_time
            lstworkval = []
            for tpline in tpl_lines:
                print "tpline:", tpline
                wname = tpline.name
                hour_id = tpline.hour_id
                quantity = tpline.quantity
                print "hour_iddddddd:", hour_id
                coefficient = hour_id.coeficient
                print "coefficient:", coefficient
                totalminutes = int(quantity * coefficient)
                print "totalminutes:", totalminutes
                end_time = addminute(time_start, totalminutes)
                fmyhour = '%.2f' % (totalminutes / 60)
                # workvals = {'time_start': time_start, 'name': wname, 'task_id': log.task_id.id, 'log_id': log.id,
                #             'is_done': False, 'hours': float(fmyhour), 'date': end_time, 'user_id': self.env.user.id}

                workvals = {'user_id': self.env.user.id, 'name': wname, 'task_id': log.task_id.id, 'log_id':  log.id,
                                       'time_end': end_time, 'unit_amount': float(fmyhour),
                                       'time_start': time_start}

                print "workvdddddnewals:", workvals
                lstworkval.append(workvals)
                work = work_obj.create(workvals)
                # print "creddddddddddddddate work:", work

                time_start = end_time

                # for myval in reversed(lstworkval):
                #     work = work_obj.create(myval)
                #     # print "creddddddddddddddate work:", work

        return True

    def fields_view_get1(self, cr, uid, view_id=None, view_type='form', context=None, toolbar=False, submenu=False):
        if context is None: context = {}
        print "wwwwwwwwwwwwwwzid:", context
        res = super(UfWorkWizard, self).fields_view_get(cr, uid, view_id=view_id, view_type=view_type, context=context,
                                                        toolbar=toolbar, submenu=False)
        if res['type'] == "form":
            print "res:", res
            # id = res['id']
            # //根据id去取得资料，并进行判断
            # if 条件成立:
            #     doc = etree.XML(res['arch'])
            #     doc.xpath("//form")[0].set("edit","false")
            #     res['arch']=etree.tostring(doc)
        return res

    @api.multi
    def _get_default_tpl(self):
        worktpl_obj = self.env['uf.work.tpl']
        # orderby = "id desc"
        orderby = "num,last_use desc"
        worktpls = worktpl_obj.search([], order=orderby)
        if len(worktpls) > 0:
            print "worktpl:", worktpls[0]
            return worktpls[0]
        else:
            return None

    @api.multi
    def _get_default_task(self):
        try:
            active_id = self.env.context['active_id']
            log_obj = self.env['uf.log']
            log = log_obj.browse(active_id)
            # print "logdddddddddd:",log

            if log:
                # print "log:", log
                # print "log.task_id.id:", log.task_id.id
                return log.task_id.id
            else:
                return None
        except:
            return None

    tpl_id = fields.Many2one('uf.work.tpl', '工作模板', default=_get_default_tpl)
    task_id = fields.Many2one('project.task', '任务', default=_get_default_task)
    # task_id = fields.Many2one('project.task', '任务')
    # begin_time = fields.Datetime(u'开始时间', default=fun_formatTime(time.strftime('%Y-%m-%d %H:%M:%S')))
    begin_time = fields.Datetime(u'开始时间', default=fields.Datetime.now())
    opmode = fields.Selection([('a', '添加'),
                               ('w', '更新'),
                               ],
                              u'操作模式', default="a")

class UfLogprintWizard(models.TransientModel):
    _name = 'uf.logprint.wizard'

    name = fields.Char('Description')

    @api.multi
    def _get_default_tpl(self):
        uflogprintwizard_obj = self.env['uf.logprint.wizard']
        orderby = "id desc"
        # orderby = "num,last_use desc"
        uflogprintwizards = uflogprintwizard_obj.search([], order=orderby)
        if len(uflogprintwizards) > 0:
            # print "uflogprintwizard:", uflogprintwizards[0]
            return uflogprintwizards[0]
        else:
            return None
        return msg

    def _get_default_snname(self):
        # vals['name'] = self.env['ir.sequence'].next_by_code('sale.order') or 'New'
        try:
            myname = self.env['ir.sequence'].next_by_code('uf.log') or '1000'
            return myname
        except:
            return None

    @api.multi
    def do_copy(self, project_id, task_id, user_id, lines):
        # uflog_obj=self.env['uf.log']
        uflogprint_obj = self.env['uf.log.print']
        uflogline_obj = self.env['uf.log.line']

        print "project_id:", project_id
        print "task_id:", task_id
        # printname = task_id.name if task_id else project_id.name
        printvals = {'note': False, 'project_id': project_id.id, 'user_id': user_id.id,
                     'name': self._get_default_snname(),
                     'task_id': task_id.id if task_id else False, 'log_id': False,
                     'print_date': time.strftime('%Y-%m-%d'), 'leave': False, 'line_ids': [], 'arrive': False}

        uflogprint_id = uflogprint_obj.create(printvals)
        print "uflogprint_id:", uflogprint_id

        #for work in lines:
        firttime,lasttime=False,False
        for work in lines[::-1]:
            if not firttime:
                firttime=work.date
            task_id = work.task_id
            # ufloglinevals = {'begin_date': work.time_start, 'user_id': user_id.id, 'name': work.name,
            #                  'end_date': work.time_end, 'print_id': uflogprint_id.id}
            #time_end=work.date + datetime.timedelta(minutes=int(work.unit_amount))
            time_end=addminute(work.date, int(work.unit_amount*60))
            lasttime=time_end
            ufloglinevals = {'begin_date': work.date, 'user_id': user_id.id, 'name': work.name,
                              'end_date': time_end, 'print_id': uflogprint_id.id}
            print "ufloglinevals:", ufloglinevals
            uflogline_obj.create(ufloglinevals)

        uflogprint_id.write({'arrive':firttime,'leave':lasttime})

        return {
            'view_type': 'form',
            'view_mode': 'form,tree',
            'res_model': 'uf.log.print',
            'res_id': uflogprint_id.id,
            'views': [(False, 'form'), (False, 'tree')],
            'type': 'ir.actions.act_window',
        }

    @api.multi
    def do_action(self):
        active_ids = dict(self._context or {}).get('active_ids', [])
        print "active_ids:", active_ids
        # check same project
        line_obj = self.env['account.analytic.line']
        lines = line_obj.browse(active_ids)
        allprjs = [line.project_id.id for line in lines]
        # print allprjs
        if len(set(allprjs)) > 1:
            raise UserError("客户日志必须选择同一个项目!")

        for line in lines:
            if not line.name:
                raise UserError("客户日志必须有名称!")

        return self.do_copy(lines[0].project_id, lines[0].task_id, lines[0].user_id, lines)
