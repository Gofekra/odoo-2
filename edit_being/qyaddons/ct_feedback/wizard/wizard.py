# -*- coding: utf-8 -*-
from odoo import api, models, fields, SUPERUSER_ID, exceptions
from odoo.osv import osv


class IssueCreationWizard(models.TransientModel):
    _name = 'ct_feedback_server.wizard.issue'

    submitter_email = fields.Char(string='Submitter email', translated=True)
    submitter_name = fields.Char(string='Submitter', translated=True)
    submitter_db = fields.Char(string='Submitter database', translated=True)
    submitter_host = fields.Char(string='Submitter\'s host', translated=True)
    info_num = fields.Char(string='Feedback number', translated=True)

    @api.model
    def report_issue(self, info_num, name, submitter_email, description, submitter_db,
              submitter_name, submitter_host, issue_stage_id):

        print '======REPORT ISSUE====='

        return self.env['project.issue'].sudo().create({
            'info_num': info_num,
            'name': name,
            'submitter_email': submitter_email,
            'description': description,
            'submitter_db': submitter_db,
            'submitter_name': submitter_name,
            'submitter_host': submitter_host,
            'issue_stage_id': issue_stage_id,
        })

    @api.model
    def create(self, vals):
        print '======CREATE======'
        print vals
        res = super(IssueCreationWizard, self).create(vals)
        return res
