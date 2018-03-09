# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.tools import html2plaintext


class RoutineTask(models.Model):

    _name = 'routine.task'
    _inherit = ['mail.thread']
    _description = ""
    _order = 'sequence'

    def _get_default_stage_id(self):
        return self.env['routine.stage'].search([('user_id', '=', self.env.uid)], limit=1)

    # name = fields.Char(string=u'工作名称',compute='_compute_name')
    name = fields.Char(string=u'工作名称')
    line_ids = fields.One2many('routine.task.line', 'routine_line_id', string='记录明细')

    priority = fields.Selection([('low', u'低'),
                                 ('mid', u'中'),
                                 ('high', u'高')],
                                string='优先级', required=True)

    user_id = fields.Many2one('res.users', string='任务执行人', default=lambda self: self.env.uid)
    memo = fields.Html('routine Content')
    sequence = fields.Integer('Sequence')
    stage_id = fields.Many2one('routine.stage', compute='_compute_stage_id',
        inverse='_inverse_stage_id', string='阶段')
    stage_ids = fields.Many2many('routine.stage', 'routine_stage_rel', 'routine_id', 'stage_id',
        string='Stages of Users',  default=_get_default_stage_id)
    open = fields.Boolean(string='Active', track_visibility='onchange', default=True)
    date_done = fields.Date('Date done')
    color = fields.Integer(string='Color Index')
    tag_ids = fields.Many2many('routine.tag', 'routine_tags_rel', 'routine_id', 'tag_id', string='标签')



    @api.depends('memo')
    def _compute_name(self):
        """ Read the first line of the memo to determine the routine name """
        for routine in self:
            text = html2plaintext(routine.memo) if routine.memo else ''
            routine.name = text.strip().replace('*', '').split("\n")[0]

    @api.multi
    def _compute_stage_id(self):
        for routine in self:
            for stage in routine.stage_ids.filtered(lambda stage: stage.user_id == self.env.user):
                routine.stage_id = stage

    @api.multi
    def _inverse_stage_id(self):
        for routine in self.filtered('stage_id'):
            routine.stage_ids = routine.stage_id + routine.stage_ids.filtered(lambda stage: stage.user_id != self.env.user)

    @api.model
    def name_create(self, name):
        return self.create({'memo': name}).name_get()[0]

    @api.model
    def read_group(self, domain, fields, groupby, offset=0, limit=None, orderby=False, lazy=True):
        if groupby and groupby[0] == "stage_id":
            stages = self.env['routine.stage'].search([('user_id', '=', self.env.uid)])
            if stages:  # if the user has some stages
                result = [{  # routines by stage for stages user
                    '__context': {'group_by': groupby[1:]},
                    '__domain': domain + [('stage_ids.id', '=', stage.id)],
                    'stage_id': (stage.id, stage.name),
                    'stage_id_count': self.search_count(domain + [('stage_ids', '=', stage.id)]),
                    '__fold': stage.fold,
                } for stage in stages]

                # routine without user's stage
                nb_routines_ws = self.search_count(domain + [('stage_ids', 'not in', stages.ids)])
                if nb_routines_ws:
                    # add routine to the first column if it's the first stage
                    dom_not_in = ('stage_ids', 'not in', stages.ids)
                    if result and result[0]['stage_id'][0] == stages[0].id:
                        dom_in = result[0]['__domain'].pop()
                        result[0]['__domain'] = domain + ['|', dom_in, dom_not_in]
                        result[0]['stage_id_count'] += nb_routines_ws
                    else:
                        # add the first stage column
                        result = [{
                            '__context': {'group_by': groupby[1:]},
                            '__domain': domain + [dom_not_in],
                            'stage_id': (stages[0].id, stages[0].name),
                            'stage_id_count': nb_routines_ws,
                            '__fold': stages[0].name,
                        }] + result
            else:  # if stage_ids is empty, get routine without user's stage
                nb_routines_ws = self.search_count(domain)
                if nb_routines_ws:
                    result = [{  # routines for unknown stage
                        '__context': {'group_by': groupby[1:]},
                        '__domain': domain,
                        'stage_id': False,
                        'stage_id_count': nb_routines_ws
                    }]
                else:
                    result = []
            return result
        return super(RoutineTask, self).read_group(domain, fields, groupby, offset=offset, limit=limit, orderby=orderby, lazy=lazy)

    @api.multi
    def _notification_recipients(self, message, groups):
        """ All users can create a new routine. """
        groups = super(RoutineTask, self)._notification_recipients(message, groups)
        new_action_id = self.env['ir.model.data'].xmlid_to_res_id('routine.action_routine_routine')
        new_action = self._notification_link_helper('new', action_id=new_action_id)
        for group, method, kwargs in groups:
            if group == 'user':
                kwargs.setdefault('actions', []).append({'url': new_action, 'title': _('New routine')})
        return groups

    @api.multi
    def action_close(self):
        return self.write({'open': False, 'date_done': fields.date.today()})

    @api.multi
    def action_open(self):
        return self.write({'open': True})


class RoutineTaskLine(models.Model):

    _name = "routine.task.line"
    _order = 'created_at'

    name = fields.Text(string='工作描述', required=True)
    created_at = fields.Datetime('执行时间', required=True)
    routine_line_id = fields.Many2one('routine.task', string='task ID')


class Stage(models.Model):

    _name = "routine.stage"
    _description = "Routine Stage"
    _order = 'sequence'

    name = fields.Char(string='名称', translate=True, required=True)
    sequence = fields.Integer(help="Used to order the routine stages", default=1)
    user_id = fields.Many2one('res.users', string='用户', required=True, default=lambda self: self.env.uid, help="Owner of the routine stage")
    fold = fields.Boolean('Folded by Default')


class Tag(models.Model):

    _name = "routine.tag"
    _description = "routine Tag"

    name = fields.Char('名称', required=True, translate=True)
    color = fields.Integer('Color Index')

    _sql_constraints = [
        ('name_uniq', 'unique (name)', "Tag name already exists !"),
    ]


