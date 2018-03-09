# -*- coding: utf-8 -*-
#!/usr/bin/env python
"""
__author__="chianggq@163.com"
__mtime__ = '2017-02-07 10:42:51'
"""
from odoo import models, fields,api
import time


# class ct_project_uf(models.Model):
#     _name = 'ct_project_uf.ct_project_uf'

#     name = fields.Char()

class UfWorkWizard(models.TransientModel):

    _name = 'uf.work.wizard'

    name = fields.Char('Description', required=True)
    #seq = fields.Char('Sequence', required=True, default=lambda self:
    #self.env['ir.sequence'].get('uf.work.wizard') or '1000')
    is_done = fields.Boolean('Done?')
    active = fields.Boolean('Active?', default=True)
    user_id = fields.Many2one('res.users', 'User',required=True, default=lambda self: self.env.user)
    last_use = fields.Datetime('LastUse',default=time.strftime('%Y-%m-%d %H:%M:%S'))
    #line_ids = fields.One2many('uf.work.wizard.line', 'tpl_id', 'Lines')
    state=fields.Selection([('draft', 'New'),
                                   ('open', 'In Progress'),
                                   ('close', 'Closed')],
                                  'Status', required=True, copy=False)
    name = fields.Char('name', required=True)
  



    def fields_view_get1(self, cr, uid, view_id=None, view_type='form', context=None, toolbar=False, submenu=False):
        if context is None:context = {}
        res = super(UfWorkWizard, self).fields_view_get(cr, uid, view_id=view_id, view_type=view_type, context=context, toolbar=toolbar,submenu=False)
        if res['type']=="form":
            print "res:",res
            #id = res['id']
            # //根据id去取得资料，并进行判断
            # if 条件成立:
            #     doc = etree.XML(res['arch'])
            #     doc.xpath("//form")[0].set("edit","false")
            #     res['arch']=etree.tostring(doc)
        return res

    @api.multi
    def _get_default_tpl(self):
        ufworkwizard_obj = self.env['uf.work.wizard']
        orderby = "id desc"
        #orderby = "num,last_use desc"
        ufworkwizards = ufworkwizard_obj.search([], order=orderby)
        if len(ufworkwizards) > 0:
            #print "ufworkwizard:", ufworkwizards[0]
            return ufworkwizards[0]
        else:
            return None
        return msg


if __name__ == "__main__":
    pass