# -*- coding: utf-8 -*-
from lxml import etree

from odoo import api, fields, models, tools, SUPERUSER_ID, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools.safe_eval import safe_eval




class ct_partner(models.Model):
    _inherit = 'res.partner'

    def _compute_same_company(self):
        for record in self:
            record.same_company = record.parent_id.id == self.env.user.parent_id.id

    def _search_same_company(self, operator, value):
        if value:
            return [('parent_id', '=', self.env.user.parent_id.id)]
        return []

    def _compute_is_employee(self):
        for record in self:
            res_users = self.env['res.users'].search([('partner_id', '=', record.id)])
            related_user = res_users[0] if len(res_users) > 0 else False
            if related_user:
                res_employees = self.env['hr.employee'].search([('user_id', '=', related_user.id)])
                is_employee = bool(res_employees[0] if len(res_employees) > 0 else False)
                print is_employee
                record.is_employee = is_employee
                record.employee = is_employee
            else:
                record.is_employee = False

    def _search_is_employee(self, operator, value):
        if value:
            employee_partners = self.env['hr.employee'].search([('user_id', '!=', False)]).mapped('user_id').mapped(
                'partner_id')
            return [('id', 'in', employee_partners.mapped('id'))]
        return []


    def _compute_task_count(self):
        for partner in self:
            partner_ids=self.env['project.project'].search_count([('partner_id','child_of',partner.id)])
            partner.project_count=partner_ids


    same_company = fields.Boolean(compute='_compute_same_company', search='_search_same_company',
                                  help='True if the partner is in the same company as the current user')
    is_employee = fields.Boolean(compute='_compute_is_employee', search='_search_is_employee',
                                 help='True if the partner is an employee')

    project_count=fields.Integer(string="项目",compute='_compute_task_count')




    def check_project(self):
        return  {
            'name': '项目',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'project.project',
            'type': 'ir.actions.act_window',
            'domain':[('partner_id','=',self.id)]
        }

