# -*- coding: utf-8 -*-
from lxml import etree

from odoo import api, fields, models, tools, SUPERUSER_ID, _
import babel.dates
import collections
from datetime import datetime, timedelta
from dateutil import parser
from dateutil import rrule
from dateutil.relativedelta import relativedelta
import logging
from operator import itemgetter
import pytz
import re
import time
import uuid

from odoo import tools
from odoo.tools.translate import _
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT
from odoo.exceptions import UserError, ValidationError





# ###################### COPIED FROM calendar.py #########################
VIRTUALID_DATETIME_FORMAT = "%Y%m%d%H%M%S"
_logger = logging.getLogger(__name__)

def calendar_id2real_id(calendar_id=None, with_date=False):
    """ Convert a "virtual/recurring event id" (type string) into a real event id (type int).
        E.g. virtual/recurring event id is 4-20091201100000, so it will return 4.
        :param calendar_id: id of calendar
        :param with_date: if a value is passed to this param it will return dates based on value of withdate + calendar_id
        :return: real event id
    """
    if calendar_id and isinstance(calendar_id, (basestring)):
        res = filter(None, calendar_id.split('-'))
        if len(res) == 2:
            real_id = res[0]
            if with_date:
                real_date = time.strftime(DEFAULT_SERVER_DATETIME_FORMAT, time.strptime(res[1], VIRTUALID_DATETIME_FORMAT))
                start = datetime.strptime(real_date, DEFAULT_SERVER_DATETIME_FORMAT)
                end = start + timedelta(hours=with_date)
                return (int(real_id), real_date, end.strftime(DEFAULT_SERVER_DATETIME_FORMAT))
            return int(real_id)
    return calendar_id and int(calendar_id) or calendar_id


def get_real_ids(ids):
    if isinstance(ids, (basestring, int, long)):
        return calendar_id2real_id(ids)

    if isinstance(ids, (list, tuple)):
        return [calendar_id2real_id(_id) for _id in ids]


def real_id2calendar_id(record_id, date):
    return '%s-%s' % (record_id, date.strftime(VIRTUALID_DATETIME_FORMAT))


def is_calendar_id(record_id):
    return len(str(record_id).split('-')) != 1
# ###################### COPIED FROM calendar.py #########################



def get_setting_value(self, property):
    return self.env['ir.values'].sudo().get_default('ct_calendar.config.settings', property)


def _get_reference_types(self):
    return [('res.partner', 'Customer'), ('project.project', 'Project')]


class Meeting(models.Model):
    _inherit = 'calendar.event'


class ProjectTask(models.Model):
    _inherit = 'project.task'

    expense_ids = fields.One2many('hr.expense', 'task_id', string='费用')
    project_state=fields.Selection([
        ('plan','项目规划'),
        ('design','蓝图设计'),
        ('construction','系统建设'),
        ('switch','上线切换'),
        ('support', '持续支持')
    ],string="项目阶段")

class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

    date=fields.Datetime(string="时间")
    sheet_ids = fields.Many2one('calendar.event','timesheet_ids')

class Project(models.Model):
    _inherit = 'project.project'

    def _compute_calendar_count(self):
        for project in self:
            partner_ids=self.env['calendar.event'].search_count([('project_id','=',project.id)])
            project.calendar_count=partner_ids

    project_state=fields.Selection([
        ('plan','项目规划'),
        ('design','蓝图设计'),
        ('construction','系统建设'),
        ('switch','上线切换'),
        ('support', '持续支持')
    ],string="项目阶段",default='plan')
    calendar_count=fields.Integer(string="项目",compute='_compute_calendar_count')

    #################
    product_line=fields.Char(string="产品线")
    product_version=fields.Char(string="产品版本")
    sale_user_id=fields.Many2one('res.partner',string="销售人员")
    sale_total=fields.Float(string="销售合同总金额")
    mplementation_total=fields.Float(string="实施费金额")
    mplementation_total_return=fields.Float(string="实施费累计回款金额")
    mplementation_start=fields.Integer(string="实施开始月份")
    mplementation_end=fields.Integer(string="实施验收月份")
    project_happening=fields.Selection([('1','正常'),('2','延期'),('3','异常')])
    manager_day=fields.Float(string="项目经理人天")
    main_mplementation_user=fields.Many2one('res.partner',string="主要实施顾问")
    main_mplementation_user_day=fields.Float(string="实施顾问人天")
    customer_day=fields.Float(string="客户确认人天")
    marks=fields.Char(string="备注")




    def check_calendar(self):
        return {
            'name': '项目',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'calendar.event',
            'type': 'ir.actions.act_window',
            'domain': [('project_id','=',self.id)],
        }




class ct_meeting(models.Model):
    _inherit = 'calendar.event'

    @api.onchange('customer_id')
    def _onchange_customer(self):
        self.contact_id = False
        return {
            'domain': {'contact_id': [('parent_id', '=', self.customer_id.id), ('parent_id', '!=', False),
                                      ('type', '=', 'contact')]},
        }

    def _is_own(self):
        for record in self:
            record.is_own = (record.create_uid.id == self.env.user.id) or self.env.user.has_group(
                'ct_calendar.group_meeting_root')

    @api.depends('user_id')
    def _is_responsible(self):
        for record in self:
            record.is_responsible = record.user_id.id == self.env.user.id

    @api.multi
    def _ct_compute_attendee(self):
        """ Returns true if the connected user is among the attendees in the meeting_ids in parameters.
        """
        for record in self:
            for attendee in record.attendee_ids:
                if self.env.user.partner_id == attendee.partner_id:
                    record.ct_is_attendee = True
                else:
                    record.ct_is_attendee = False

    @api.multi
    def _compute_visible_to_user(self):
        # print '#### _compute_visible_to_user ###'
        for record in self:

            record.ct_visible_to_user = \
                record.is_own or \
                record.is_responsible or \
                record.ct_is_attendee or \
                (self.env.uid in (get_setting_value(self, 'meeting_pmo_group_users') or [])) or \
                self.env.user.has_group('ct_calendar.group_meeting_root') or \
                (record.sudo().project_id and (record.sudo().project_id.user_id == self.env.user) or False)
            # self.env.user.has_group('ct_calendar.group_pmo') or \



    @api.model
    def search(self, args, offset=0, limit=None, order=None, count=False):
        if self._context.get('mymeetings'):
            args += [('partner_ids', 'in', self.env.user.partner_id.ids)]

        new_args = []
        for arg in args:
            new_arg = arg
            if arg[0] in ('stop_date', 'stop_datetime', 'stop',) and arg[1] == ">=":
                if self._context.get('virtual_id', True):
                    new_args += ['|', '&', ('recurrency', '=', 1), ('final_date', arg[1], arg[2])]
            elif arg[0] == "id":
                new_arg = (arg[0], arg[1], get_real_ids(arg[2]))
            new_args.append(new_arg)

        if not self._context.get('virtual_id', True):
            return super(Meeting, self).search(new_args, offset=offset, limit=limit, order=order, count=count)

        events = super(Meeting, self).search(new_args, offset=0, limit=0, order=None, count=False).filtered(lambda r: r.ct_visible_to_user is True)
        events = self.browse(events.get_recurrent_ids(args, order=order))

        if count:
            return len(events)
        elif limit:
            return events[offset: offset + limit]
        return events


    @api.model
    def create(self, vals):
        meeting = super(Meeting, self).create(vals)
        followers_partner_ids = meeting.message_follower_ids.mapped('partner_id.id')
        group_ids = get_setting_value(self, 'meeting_followers_groups')
        ResGroups = self.env['res.groups']
        Followers = self.env['mail.followers']
        if group_ids:
            for group_id in group_ids:
                partner_ids = ResGroups.browse(group_id).users.mapped('partner_id.id')
                for id in partner_ids:
                    if id not in followers_partner_ids:
                        Followers.create({
                            'res_model': self._name,
                            'res_id': meeting.id,
                            'partner_id': id
                        })

        if meeting.sudo().project_id:
            project_manager = meeting.sudo().project_id and meeting.sudo().project_id.user_id or False
            if project_manager and project_manager.partner_id:
                if project_manager.partner_id.id not in meeting.message_follower_ids.mapped('partner_id.id'):
                    Followers.create({
                        'res_model': self._name,
                        'res_id': meeting.id,
                        'partner_id': project_manager.partner_id.id
                    })
        return meeting


    @api.multi
    def write(self, values):
        Followers = self.env['mail.followers']
        for meeting in self:
            if len(values) == 1 and values.has_key('message_follower_ids'):
                pass
            else:
                # if self.env.user.partner_id not in meeting.partner_ids and (not values.has_key('message_follower_ids') and len(values)==1):
                # if self.env.user.partner_id not in meeting.partner_ids and not meeting.is_own:
                #     raise UserError(_('Only the attendees can edit the meeting.'))

                if (not meeting.ct_is_attendee) and \
                        (not meeting.is_responsible) and \
                        (not meeting.is_own) and \
                        (not meeting.env.user.has_group('ct_calendar.group_meeting_root')):
                    raise UserError(_('You are not allowed to perform this action. '
                                      'Contact your Administrator if you think there is an error.'))

            super(Meeting, meeting).write(values)

            if values.has_key('project_id'):
                project_manager = meeting.sudo().project_id and meeting.sudo().project_id.user_id or False
                if project_manager and project_manager.partner_id:
                    if project_manager.partner_id not in meeting.message_follower_ids.mapped('partner_id'):
                        Followers.create({
                            'res_model': self._name,
                            'res_id': meeting.id,
                            'partner_id': project_manager.partner_id.id
                        })
        return True


    @api.multi
    def unlink(self):
        for meeting in self:
            if (not meeting.ct_is_attendee) and \
                    (not meeting.is_responsible) and \
                    (not meeting.is_own) and \
                    (not meeting.env.user.has_group('ct_calendar.group_meeting_root')):
                raise UserError(_('You are not allowed to perform this action. '
                                  'Contact your Administrator if you think there is an error.'))
            super(ct_meeting, meeting).unlink()
        return True


    REF_TYPES = [('customer', 'Customer'), ('project', 'Project')]
    STAGES = [('normal', 'Normal'), ('postponed', 'Postponed'), ('canceled', 'Canceled')]
    PRIVACY = [('public', 'Everyone'), ('private', 'Only me'), ('confidential', 'Only internal users'),
               ('followers', 'Followers only')]


    def _compute_timesheet_ids(self):
        result=[]
        for line in self:
            for res in line.task_id:
                result.append(res.id)
        timesheet_ids=self.env['account.analytic.line'].search([('task_id','in',result)])
        expense_ids=self.env['hr.expense'].search([('task_id','in',result)])
        self.expense_ids=expense_ids
        self.timesheet_ids=timesheet_ids

    customer_id = fields.Many2one('res.partner', string='Customer', translated=True, domain=[('is_company', '=', True)])
    customer_name = fields.Char(string='Customer name', translated=True, related='customer_id.name')
    expense_ids = fields.One2many('hr.expense', 'meeting_id', string='Expenses', translated=True,compute=_compute_timesheet_ids)
    stage = fields.Selection(STAGES, translated=True, index=True, default='normal')
    is_own = fields.Boolean(compute='_is_own', help='If the meeting was created by the current user')
    is_responsible = fields.Boolean(compute='_is_responsible', help='If the current user is responsible of the meeting')
    ct_is_attendee = fields.Boolean('Attendee', compute='_ct_compute_attendee',
                                    help='True if the current user is an attendee of that meeting')
    project_id = fields.Many2one('project.project', string='Project', tranlated=True)
    ct_visible_to_user = fields.Boolean(compute='_compute_visible_to_user')
    contact_id = fields.Many2one('res.partner', string='Contact', translated=True,
                                 domain=[('parent_id', '=', 'customer_id'), ('type', '=', 'contact')])
    contact_phone = fields.Char(string='Contact Phone', related='contact_id.phone', readonly=True, tranlated=True)
    contact_mobile = fields.Char(string='Contact Mobile', related='contact_id.mobile', readonly=True, tranlated=True)
    task_id=fields.Many2many('project.task','calendar_project_task','calendar_id','task_ids',string="任务")
    timesheet_ids = fields.One2many('account.analytic.line', 'sheet_ids',string='日志记录', readonly=True,compute=_compute_timesheet_ids)
    event_state=fields.Selection([('draft','草稿'),('complute', '完成'),],string="任务分配",deafult='draft')
    project_state=fields.Selection([
        ('plan','项目规划'),
        ('design','蓝图设计'),
        ('construction','系统建设'),
        ('switch','上线切换'),
        ('support', '持续支持')
    ],string="项目阶段",related="project_id.project_state")



    def commit_task(self):
        task_ids=[]
        for partner_id in self.partner_ids:
            user_id=self.env['res.users'].search([('partner_id','=',partner_id.id)])
            vals={
                'name':self.name,
                'project_id': self.project_id.id,
                'user_id': user_id.id,
                'planned_hours': self.duration,
                'partner_id': self.customer_id.id,
            }
            print vals
            task_id=self.env['project.task'].create(vals)
            task_ids.append(task_id.id)

        print task_ids
        self.task_id =[(6, 0,task_ids)]
        self.event_state='complute'




    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        res = super(ct_meeting, self).fields_view_get(
            view_id=view_id, view_type=view_type, toolbar=toolbar, submenu=submenu)
        if 'customer_id' in res['fields'] and not self.env.user.has_group('ct_base_local.group_customer_ir'):
            doc = etree.XML(res['arch'])
            for node in doc.xpath("//field[@name='customer_id']"):
                node.set('domain', "['|','&',('is_company', '=', True),('user_parner_id', 'in', %s),('user_id', '=', %s)]" % (self.env.uid,self.env.uid))
            res['arch'] = etree.tostring(doc)
        return res






class ct_attendee(models.Model):
    _inherit = 'calendar.attendee'




class ct_expense(models.Model):
    _inherit = 'hr.expense'

    @api.depends('meeting_id', 'meeting_id.customer_id')
    def _compute_customer_id(self):
        for expense in self:
            if len(expense.mapped('meeting_id')) == 1:
                expense.customer_id = expense.meeting_id.customer_id.id


    @api.depends('meeting_id', 'meeting_id.description')
    def _compute_description(self):
        for expense in self:
            if len(expense.mapped('meeting_id')) == 1:
                expense.description = expense.meeting_id.description


    def _search_customer_id(self, operator, value):
        return [('meeting_id.customer_id', operator, value)]



    meeting_id = fields.Many2one('calendar.event', string='Meeting', translated=True)
    customer_id = fields.Many2one('res.partner', compute='_compute_customer_id', search='_search_customer_id',
                                  string='Customer', translated=True, store=True)

    description=fields.Char(string='description',translated=True, compute='_compute_description',)

    task_id=fields.Many2one('project.task','expense_ids')




class MeetingCleanupWizard(models.TransientModel):
    _name = 'ct_calendar.event_clean.wizard'

    @api.model
    def update_records(self):
        res = self.env['calendar.event']._search([('privacy', '=', 'followers')])
        if res:
            self.env.cr.execute('''UPDATE calendar_event SET privacy='public' WHERE id in %s''', (tuple(res),))
        return



class EditCustomer(models.Model):
    _name='edit.customer'

    event_id=fields.Char(string="日程")
    customer_id=fields.Many2one('res.partner',string='客户')


    def send_edit(self):
        event_id=re.findall(r"\d+\.?\d*", str(self.event_id))
        calendar_id=self.env['calendar.event'].search([('id','in',event_id)])
        for event_ids  in   calendar_id:
            event_ids.customer_id=self.customer_id.id
