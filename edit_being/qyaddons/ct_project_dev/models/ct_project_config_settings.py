# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, tools, SUPERUSER_ID, _


class ProjectConfiguration(models.TransientModel):
    _name = 'ct_project.config.settings'
    _inherit = 'res.config.settings'
    
    @api.multi
    def _default_get_script_path(self):
        if self.env['ir.values'].sudo().get_default('ct_project.config.settings', 'ct_project_svn_script_path'):
            return self.env['ir.values'].sudo().get_default('ct_project.config.settings', 'ct_project_svn_script_path')
        return 'odoo_getaddon_script.sh'
    
    @api.multi
    def _default_get_addons_directory(self):
        if self.env['ir.values'].sudo().get_default('ct_project.config.settings', 'ct_project_addons_directory'):
            return self.env['ir.values'].sudo().get_default('ct_project.config.settings', 'ct_project_addons_directory')
        return '/data/saas/co-addons'
    
    @api.multi
    def _default_get_logs_directory(self):
        if self.env['ir.values'].sudo().get_default('ct_project.config.settings', 'ct_project_logs_directory'):
            return self.env['ir.values'].sudo().get_default('ct_project.config.settings', 'ct_project_logs_directory')   
        return '/data/saas/log' 
    
    @api.multi
    def _default_get_upload_stage(self):
        if self.env['ir.values'].sudo().get_default('ct_project.config.settings', 'ct_project_upload_stage'):
            value = self.env['ir.values'].sudo().get_default('ct_project.config.settings', 'ct_project_upload_stage')
            if value:
                return value
        return self.env.ref('ct_project_dev.test').id

    @api.multi
    def _default_get_issue_upload_stage(self):
        if self.env['ir.values'].sudo().get_default('ct_project.config.settings', 'ct_project_issue_upload_stage'):
            return self.env['ir.values'].sudo().get_default('ct_project.config.settings', 'ct_project_issue_upload_stage')
        return self.env.ref('ct_project_dev.issue_verifying_stage').id
    
    @api.multi
    def _default_get_auto_install(self):
        return self.env['ir.values'].sudo().get_default('ct_project.config.settings', 'ct_project_auto_install')  
        
    script_path = fields.Char(string='SVN Script path', default=lambda self: self._default_get_script_path())
    addons_directory = fields.Char(string='Addons directory', default=lambda self: self._default_get_addons_directory())
    logs_directory = fields.Char(string='logs directory', default=lambda self: self._default_get_logs_directory())
    upload_stage = fields.Many2one('project.task.type', string='Task transfer stage',
                                   help='Stage where the project(module) is to be transfered',
                                   default=lambda self: self._default_get_upload_stage())
    issue_upload_stage = fields.Many2one('project.issue.stage', string='Issue transfer stage',
                                   help='Stage where the project(module) linked to the issue is to be transfered',
                                   default=lambda self: self._default_get_issue_upload_stage())
    auto_install = fields.Boolean(string='Auto-Install', default=lambda self: self._default_get_auto_install(), help='Install automatically the module after the transfer')
    
    @api.multi
    def set_script_path_defaults(self):
        return self.env['ir.values'].sudo().set_default(
            'ct_project.config.settings', 'ct_project_svn_script_path', self.script_path)

    @api.multi
    def set_addons_directory_defaults(self):
        return self.env['ir.values'].sudo().set_default(
            'ct_project.config.settings', 'ct_project_addons_directory', self.addons_directory)
        
    @api.multi
    def set_logs_directory_defaults(self):
        return self.env['ir.values'].sudo().set_default(
            'ct_project.config.settings', 'ct_project_logs_directory', self.logs_directory)
    
    @api.multi
    def set_upload_stage_defaults(self):
        return self.env['ir.values'].sudo().set_default(
            'ct_project.config.settings', 'ct_project_upload_stage', self.upload_stage.id)

    @api.multi
    def set_issue_upload_stage_defaults(self):
        return self.env['ir.values'].sudo().set_default(
            'ct_project.config.settings', 'ct_project_issue_upload_stage', self.issue_upload_stage.id)
        
    @api.multi
    def set_auto_install_defaults(self):
        return self.env['ir.values'].sudo().set_default(
            'ct_project.config.settings', 'ct_project_auto_install', self.auto_install)        
        
        
