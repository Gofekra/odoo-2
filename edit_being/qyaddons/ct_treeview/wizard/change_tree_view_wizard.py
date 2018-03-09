# -*- coding: utf-8 -*-
import odoo
from odoo.osv import  osv
from odoo.osv import orm
from lxml import etree
from odoo import SUPERUSER_ID
from collections import defaultdict    
from odoo import models, tools, api,fields



class view(models.Model):
    _inherit = 'ir.ui.view'

    customized_for=fields.Many2one('res.users','Customized For')
    default_view1=fields.Boolean('Default View',default=True)
    customized_view=fields.Boolean('Customized View',default=False)



class ir_model_fields(models.Model):
    _inherit = 'ir.model.fields'

    sequence= fields.Integer('Sequence', help="Gives the sequence order when displaying a list.")
    state=fields.Selection([('manual','Custom Field'),('base','Base Field'),('changetree','Changed from tree')],'Type',default
                           =lambda self,cr,uid,ctx=None: (ctx and ctx.get('manual',False)) and 'manual' or 'changetree')

    _order = 'sequence'


    @api.returns('self') #If we keep @api.v7, we have to add @api.v8 code too.
    def write(self,values):
        if values.get('sequence',False):
            res = super(models.Model, self).write(values)
        else:
            res = super(ir_model_fields, self).write(values)
        return res

class change_tree_view_wizard(models.Model):

    _name = 'change.tree.view.wizard'

    model_id=fields.Many2one('ir.model', 'Object',track_visibility='onchange')
    custom_tree_fields_ids=fields.Many2many('ir.model.fields',
                                            'new_model_obj_rel', 'change_id', 'new_fields_id' , 'New Fields',track_visibility='onchange')
    view_xml_id= fields.Integer('Current View ID')
    state_visible= fields.Selection([
        ('state_visible','Visible in list view'),
        ('state_invisible','Invisible in list view')
    ],string="State Visibility",default='state_visible')


    def change_tree_process(self,original_arch):
        model_fields_pool = self.env['ir.model.fields']
        model_id = self.model_id.id
        state_flag = self.state_visible
        search_clause = [('model_id','=',model_id), ('name','=','state')]
        search_field_state = model_fields_pool.sudo().search(search_clause)

        exported_arch = ''
        arch_with_no_seq = ''
        _exported_arch_lst = """<tree string="Exported Tree">\n """
        for record in self:
            for new_fields in record.custom_tree_fields_ids:
                if new_fields.name == 'state':
                    continue
                if new_fields.sequence:
                    exported_arch += '<field name="%s" modifiers="{}"/>\n' %new_fields.name
                else:
                    arch_with_no_seq += '<field name="%s" modifiers="{}"/>\n' %new_fields.name
                #exported_arch += '<field name="%s" modifiers="{}"/>' %new_fields.name
        exported_arch += arch_with_no_seq

        if search_field_state:
            if state_flag == 'state_visible':
                exported_arch += '<field name="state" invisible="0"/>'
            else:
                exported_arch += '<field name="state" invisible="1"/>'

        _exported_arch_lst += """ %s """ %exported_arch
        _exported_arch_lst += """ </tree> """
        new_arch = etree.fromstring(self.encode(_exported_arch_lst))

        for new_arch_f in new_arch:
            for new_fields in self.custom_tree_fields_ids:
                if new_arch_f.attrib['name'] == str(new_fields.name):
                    for original_field in original_arch:
                        # Old Code # original_field.attrib['name'] == str(new_fields.name):
                        if type(original_field) != etree._Comment and original_field.attrib['name'] == str(new_fields.name):
                            if 'groups' in original_field.attrib:
#                                 can_see = self.user_has_groups(cr, uid,groups=original_field.get('groups'),context=context)
#                                 if not can_see:
#                                     raise osv.except_osv(('Select Error!'), ("Sorry You can't see this field as you not have privilage! "+ new_arch_f.attrib['name']))
                                new_arch_f.set('groups', original_field.get('groups'))
                            if 'attrs' in original_field.attrib:
                                new_arch_f.set('attrs',original_field.attrib.get('attrs'))
                                # Old Code # new_arch_f.set('attrs',attrs.attrib['attrs'])
                            if 'sum' in original_field.attrib:
                                new_arch_f.set('sum', original_field.get('sum'))
                            if 'invisible' in original_field.attrib:
                                new_arch_f.set('invisible', original_field.get('invisible'))
                            if 'widget' in original_field.attrib:
                                new_arch_f.set('widget', original_field.get('widget'))
                            if 'string' in original_field.attrib:
                                new_arch_f.set('string', original_field.get('string'))
                            if 'modifiers' in original_field.attrib:
                                new_arch_f.set('modifiers', original_field.get('modifiers'))
        return etree.tostring(new_arch, encoding="utf-8")

    def refresh_page(self):
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }
    def check_user_change_tree_group(self):
        model_data_pool = self.env['ir.model.data']
        change_tree_group_id = model_data_pool.get_object_reference('ct_treeview', 'group_change_tree')[1]
        for group in self.env['res.users'].browse(self.env.uid).groups_id:
            if group.id == change_tree_group_id:
                return True
        return False
    def encode(self, s):
        if isinstance(s, unicode):
            return s.encode('utf8')
        return s

    def check_group(self, node):
        if node.get('groups'):
            can_see = self.user_has_groups(groups=node.get('groups'))
            if not can_see:
                node.set('invisible', '1')
                modifiers['invisible'] = True
                if 'attrs' in node.attrib:
                    del(node.attrib['attrs']) #avoid making field visible later
            del(node.attrib['groups'])
        return True

    def change_tree_view(self):
        if not self.check_user_change_tree_group():
            raise osv.except_osv(('Sorry Access Denied!'), ("Sorry Access Denied ... Ask your system administrator!"))
        if not self.state_visible:
            raise osv.except_osv(('Invalid Data!'), ("Please Select State Visibility!"))

        seq_list = [x.sequence for x in self.custom_tree_fields_ids]
        max_seq=0
        if seq_list:
            max_seq = max(list(set(seq_list)))
        for element in self.custom_tree_fields_ids:
            if element.sequence < 1:
                max_seq += 1
                self.env.cr.execute('UPDATE ir_model_fields ' \
                        'SET sequence = %s WHERE id in %s', (max_seq, tuple([element.id])))
        view_id = self.view_xml_id
        view_data_id = False
        if view_id:
            view_data_id = self.env['ir.ui.view'].sudo().search([
                ('type','=','tree'),('id','=',view_id),
                ('default_view1','=',True),
                ('customized_view','!=',True),
                 ('customized_for','=',None)
            ])
        if view_data_id:
                original_view_arch = self.env['ir.ui.view'].browse(view_data_id.id).arch
                original_arch = etree.fromstring(self.encode(original_view_arch))
                final_arch = self.change_tree_process(original_arch)
                view_objs = self.env['ir.ui.view'].browse(view_data_id.id)
                view_vals={
                           'arch':final_arch,
                           'type':'tree',
                           'inherit_id': view_objs.inherit_id.id,
                           'model':view_objs.model,
                           'name':view_objs.name,
                           'customized_for':self.env.uid,
                           'default_view1':False,
                           'customized_view':True
                           }
                new_view_id = self.env['ir.ui.view'].create(view_vals)
                return {
                        'type':'ir.actions.client',
                        'tag':'reload',
                        }
#                 return self.refresh_page(cr, uid, ids, context)
        else:
            #create new record with create_uid = uid and write_uid = uid
            model_name = self.model_id.model
            view_data_id = self.env['ir.ui.view'].sudo().search([
                ('type','=','tree'),('model','=',str(model_name)),
                 ('default_view1','=',False),('customized_view','=',True),
                  ('customized_for','=',self.env.uid)])
            if view_data_id:
                original_view_arch = self.env['ir.ui.view'].browse(view_data_id.id).arch
                original_arch = etree.fromstring(self.encode(original_view_arch))
                final_arch = self.change_tree_process(original_arch)
                view_data_id.write({'arch':final_arch,'customized_for':self.env.uid, 'default_view1':False,'customized_view':True})
                return self.refresh_page()
        return True


    @api.model
    def open_action(self,args,context):
        tree_view_id = args[0]
        model_name = args[1]
        view_fields = args[2]
        current_view_fields = []
        model_id = self.env['ir.model'].sudo().search( [('model', '=', str(model_name))])
        model_fields_pool = self.env['ir.model.fields']
        if 'state' in view_fields:
            view_fields.pop('state')
            context.update({'state_show': '1'})
        for field in view_fields:
            # print field
            search_clause = [('model_id','=',model_id.id), ('name','=',field)]
            model_field_id = model_fields_pool.sudo().search(search_clause,order="sequence")
            if model_field_id:
                current_view_fields.append(model_field_id.id)

        #根据字段sequence进行排序
        search_clause1 = [('id', 'in', current_view_fields)]
        model_field_id1 = model_fields_pool.sudo().search(search_clause1, order="sequence")
        current_view_fields1=[]
        for res_id in model_field_id1:
            current_view_fields1.append(res_id.id)
        form_view_id = self.env.ref('ct_treeview.view_change_tree_view_wizard').id,
        for view_id in  form_view_id:
            view_id=view_id
        ctx = dict(context)
        ctx.update({
            'default_model_id': model_id.id,
            'default_view_xml_id': tree_view_id,
            'default_custom_tree_fields_ids': current_view_fields1,
        })

        return {
            'name': 'Customize your tree appearance',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'change.tree.view.wizard',
            'views': [(view_id, 'form')],
            'view_id':view_id,
            'type': 'ir.actions.act_window',
            'target': 'new',
            'context': ctx,
        }



    #恢复初始tree视图
    @api.model
    def recovery_action(self,view_id):
        view_id=self.env['ir.ui.view'].browse(view_id)
        if view_id.customized_for and view_id.customized_for.id==self.env.uid:
            view_id.unlink()
        return True


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
    
