# -*- coding: utf-8 -*-
from odoo import api, models, fields, SUPERUSER_ID, _
from odoo.exceptions import UserError, ValidationError
from odoo.osv import osv
import xmlrpclib


class FeedbackStage(models.Model):
    _name = 'ct_feedback_server.feedback.stage'
    _order = 'sequence'

    name = fields.Char(string='Name', translated=True)
    sequence = fields.Integer(string='Sequence', translated=True)
    fold = fields.Boolean(string='Folded', translated=True)


class Issue(models.Model):
    _inherit = 'project.issue'

    @api.multi
    def handle(self):
        for rec in self:
            if rec.feedback_stage_id == self.env.ref('ct_feedback_server.feedback_stage_unsolved'):
                rec.write({
                    'discarded': False,
                    'user_id': self.env.uid,
                    'feedback_stage_id': self.env.ref('ct_feedback_server.feedback_stage_inprocess').id,
                    'notify_feedback_state_change': 'handled'
                })
        return

    @api.multi
    def discard(self):
        for rec in self:
            if (rec.user_id != self.env.user) and (self.env.uid != SUPERUSER_ID):
                raise UserError(_("Only concerned user can do this operation. "
                                  "Please contact your administrator if you think there is an error."))

            if rec.feedback_stage_id == self.env.ref('ct_feedback_server.feedback_stage_inprocess'):
                rec.write({
                    'discarded': True,
                    'fixed': False,
                    'user_id': False,
                    'feedback_stage_id': self.env.ref('ct_feedback_server.feedback_stage_unsolved').id,
                    'notify_feedback_state_change': 'submitted'
                })
        return

    @api.multi
    def engage_discussion(self):
        # TODO: ALLOW ONLY THE HANDLER TO START THE DISCUSSION
        # print self[0].im_chat_url
        # return {
        #     "type": "ir.actions.act_url",
        #     "url": self[0].im_chat_url,
        #     "target": "new",
        # }
        self.ensure_one()
        ir_model_data = self.env['ir.model.data']
        compose_form_id = ir_model_data.get_object_reference('mail', 'email_compose_message_wizard_form')[1]
        template_id = ir_model_data.get_object_reference('ct_feedback_server', 'feedback_reply_template')[1]
        ctx = dict(self.env.context or {})
        ctx.update({
            'default_model': 'project.issue',
            'default_res_id': self.ids[0],
            'default_use_template': bool(template_id),
            'default_template_id': template_id,
            'default_composition_mode': 'comment',
        })
        return {
            'name': _('Compose Email'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(compose_form_id, 'form')],
            'view_id': compose_form_id,
            'target': 'new',
            'context': ctx,
        }


    @api.multi
    def assign(self):
        if self[0].feedback_stage_id == self.env.ref('ct_feedback_server.feedback_stage_solved'):
            raise UserError(_("You cannot assign an already solved feedback!"))
        return {
            'name': 'Assign feedback to user',
            'type': 'ir.actions.act_window',
            'res_model': 'ct_feedback_server.wizard.issue',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_operation_type': 'assign',
                'default_feedback_id': self[0].id,
            }
        }

    @api.multi
    def solve(self):
        # if (self[0].user_id != self.env.user) and (self.env.uid != SUPERUSER_ID):
        if self[0].user_id != self.env.user:
            raise UserError(_("Only concerned user can do this operation. "
                              "Please contact your administrator if you think there is an error."))
        return {
            'name': 'Solve feedback',
            'type': 'ir.actions.act_window',
            'res_model': 'ct_feedback_server.wizard.issue',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_operation_type': 'fix',
                'default_feedback_id': self[0].id,
                'default_user_id': self.env.uid,
            }
        }

    def _prepare_discard_data(self, vals):
        vals['discarded'] = True
        vals['user_id'] = False
        # vals['fix_date'] = False
        vals['fixed'] = False
        # vals['fixed_by'] = False
        vals['notify_feedback_state_change'] = 'submitted'

    @api.multi
    def _compute_current_user(self):
        for rec in self:
            rec.current_uid = self.env.uid

    @api.multi
    def _compute_kanban_user_id(self):
        for rec in self:
            rec.kanban_user_id = rec.user_id and rec.user_id.id or 0

    @api.multi
    def _compute_solvable(self):
        for rec in self:
            rec.solvable = rec.feedback_stage_id and (
            rec.feedback_stage_id == self.env.ref('ct_feedback_server.feedback_stage_inprocess')) or False

    @api.multi
    def _check_user_right(self, object, action=None):
        ACTION_LIST = ['discard', 'handled', 'submitted', 'handle', 'fix', 'solved']
        if action in ACTION_LIST:
            if (object.user_id != self.env.user) and (self.env.uid != SUPERUSER_ID):
                raise UserError(_("Only concerned user can do this operation. "
                                  "Please contact your administrator if you think there is an error."))
        elif action == None:
            if self.env.uid != SUPERUSER_ID:
                raise UserError(_("Action forbidden to simple user; You may get in touch with your administrator"))

    def _default_feedback_stage(self):
        stage = self.env.ref('ct_feedback_server.feedback_stage_unsolved', raise_if_not_found=False)
        return stage and stage.id or False

    def _compute_form_link(self):
        for record in self:
            # id=3&view_type=form&model=ct_feedback_client.question&action=166
            record.form_link = "%s/web/#id=%s&view_type=form&model=ct_feedback_client.question" % (record.submitter_host, record.info_id)

    @api.model
    def _read_group_feedback_stage_ids(self, stages, domain, order):
        return stages.sudo().search([])

    write_uid = fields.Many2one('res.users', string='Discarded by', translated=True)
    fixed_by = fields.Many2one('res.users', string='Fixed by', translated=True)
    submitter_email = fields.Char(string='Submitter email', translated=True)
    submitter_name = fields.Char(string='Submitter', translated=True)
    submitter_db = fields.Char(string='Submitter database', translated=True)
    submitter_host = fields.Char(string='Submitter\'s host', translated=True)
    info_num = fields.Char(string='Feedback number', translated=True)
    info_id = fields.Integer(string='Feedback id', translated=True)

    submitter_ip = fields.Char(string='Submitter ip address', translated=True)
    submitter_county = fields.Char(string='Submitter country', translated=True)
    submitter_os = fields.Char(string='Submitter OS', translated=True)
    submitter_language = fields.Char(string='Submitter language', translated=True)
    submitter_resolution = fields.Char(string='Submitter resolution', translated=True)
    submitter_browser = fields.Char(string='Submitter resolution', translated=True)

    form_link = fields.Char(compute='_compute_form_link')
    description = fields.Html()
    is_feedback = fields.Boolean(string='Feedback', help='If this issue is a feedback from the remote client',
                                 translated=True)
    discarded = fields.Boolean(string='Discarded', help='If this issue has been discarded', tranlated=True)
    fixed = fields.Boolean(string='Fixed', help='If this issue has been fixed', tranlated=True)
    fix_date = fields.Datetime(string='Fixed on', help='Date of fixing', readonly=True, tranlated=True)
    fix_description = fields.Html(string='Fixing explanation', translated=True)
    feedback_stage_id = fields.Many2one('ct_feedback_server.feedback.stage',
                                        'Feedback stage',
                                        readonly=False,
                                        track_visibility='onchange',
                                        group_expand='_read_group_feedback_stage_ids',
                                        default=lambda self: self._default_feedback_stage(),
                                        translated=True)
    sequence = fields.Integer(string='Sequence', translated=True)
    current_uid = fields.Integer(compute='_compute_current_user', store=False)
    kanban_user_id = fields.Integer(compute='_compute_kanban_user_id', store=False)
    solvable = fields.Boolean(compute='_compute_solvable', store=False)
    # priority = fields.Selection(attrs={'readonly':['|',('discarded','=',True),('feedback_stage_id','=', lambda self: self.env.ref('ct_feedback.feedback_stage_solved').id)]})
    im_chat_url = fields.Char(string='Feedback instant message url')

    # ------------------------------
    # CRUD OVERRIDING
    # ------------------------------
    @api.multi
    def write(self, vals):

        if self.is_feedback:

            # Impossible to change the description of the feedback submitted by customer
            # TODO: Maybe Excepted the feedback_agent
            if 'description' in vals: del vals['description']

            if 'priority' in vals and (self.discarded or self.fixed):
                if self.fixed:
                    del vals['priority']
                elif not self.env.user.has_group('project.group_project_manager'):
                    del vals['priority']

            unsolved_stage = self.env.ref('ct_feedback_server.feedback_stage_unsolved')
            inprocess_stage = self.env.ref('ct_feedback_server.feedback_stage_inprocess')
            solved_stage = self.env.ref('ct_feedback_server.feedback_stage_solved')

            stages = {
                unsolved_stage.id: unsolved_stage,
                inprocess_stage.id: inprocess_stage,
                solved_stage.id: solved_stage,
            }

            '''
            CONTROLS IN CASE THE STAGE IS CHANGED USING THE KANBAN
            '''
            if self.env.context.get('from_kanban') and 'feedback_stage_id' in vals:
                new_feedback_stage = stages[vals['feedback_stage_id']]

                if self.feedback_stage_id == unsolved_stage:
                    '''IF NEW STAGE IS INPROCESSING: NOTIFY HANDLING'''
                    if new_feedback_stage == inprocess_stage:
                        vals['discarded'] = False
                        vals['user_id'] = self.env.uid
                        vals['notify_feedback_state_change'] = 'handled'
                    else:
                        '''ELSE RAISE EXCEPTION: IMPOSSIBLE TO MOVE DIRECTLY TO ANY OTHER STAGE'''
                        raise UserError(_("You cannot move directly a feedback from '%s' to '%s'" % (
                        unsolved_stage.name, new_feedback_stage.name)))

                elif self.feedback_stage_id == inprocess_stage:
                    '''IF NEW STAGE IS UNSOLVED: NOTIFY DISCARD'''
                    '''BUT BEFORE CHECK IF THE USER IS THE RESPONSIBLE'''

                    self._check_user_right(object=self, action="discard")

                    if new_feedback_stage == unsolved_stage:
                        self._prepare_discard_data(vals)

                    elif new_feedback_stage == solved_stage:
                        '''ELSE RAISE EXCEPTION: IMPOSSIBLE TO MOVE TO SOLVED BY DRAGGING'''
                        raise UserError(_("It is not allowed to move a feedback to '%s' by dragging; "
                                          "You may click on the button 'Solve' (Displayed in Form mode if the current user is responsible of the related feedback)" % solved_stage.name))
                elif self.feedback_stage_id == solved_stage:
                    # if not self.env['res.users'].has_group('project.group_project_manager'):
                    self._check_user_right(object=self, action=None)

                    '''IF NEW STAGE IS UNSOLVED: NOTIFY DISCARD IF USER IS ROOT'''
                    if new_feedback_stage == unsolved_stage:
                        self._prepare_discard_data(vals)
                    else:
                        '''ELSE RAISE EXCEPTION: IMPOSSIBLE TO MOVE DIRECTLY TO ANY OTHER STAGE'''
                        raise UserError(_("You cannot move directly a feedback from '%s' to '%s'" % (
                            solved_stage.name, new_feedback_stage.name)))
            else:
                """
                CONTROLS IN CASE THE USER JUST USED THE WIZARDS TO CHANGE THE STAGE
                """
                if 'notify_feedback_state_change' in vals:
                    self._check_user_right(object=self, action=vals['notify_feedback_state_change'])

        result = super(Issue, self).write(vals)

        if self.is_feedback:
            database = self.submitter_db
            url = self.submitter_host
            question_num = self.info_num

            if 'notify_feedback_state_change' in vals:
                r = self.env['ct_feedback_server.feedback.wizard'].notify_feedback_state_change(
                    database=database, url=url, question_num=question_num,
                    new_state=vals['notify_feedback_state_change'], update_data=vals.get('notify_feedback_data', {}))
                if not r:
                    raise UserError(_("An error occurred while reporting the feedback status change to '%s'." % url))
        return result
