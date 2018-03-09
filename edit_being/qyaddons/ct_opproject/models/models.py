# -*- coding: utf-8 -*-

from odoo import models, fields, api,_
import datetime
from odoo.exceptions import UserError
class opproject(models.Model):
    _inherit = "account.payment"


    def post(self):
        sales_id = self.env['sale.order'].search([('name', '=', self.communication)])
        for lin_id in sales_id.order_line:
            sale_line_id= lin_id.id
            task_id = self.env['project.task'].search([('sale_line_id', '=', sale_line_id)])
            if task_id:
                task_val = self.env['project.task'].browse(task_id.id)
                task_val.write({'stage_id': int(task_val.stage_id.id+1)})
        super(opproject,self).post()



class res_partner(models.Model):
    _inherit = "res.partner"
    owner_name= fields.Char(string="业主姓名")
    owner_mobile = fields.Char(string="业主电话")
    customer_name = fields.Char(string="来源渠道")
    manager_name = fields.Char(string="项目经理名字")
    house_type= fields.Char(string="户型")
    area=fields.Char(string="面积")


class Sale_Orderline(models.Model):
    _inherit = "sale.order"

    def _get_child_bom_lines(self):
        bom_obj = self.env['project.task']
        for bom_line in self:
            for order_line in bom_line.order_line:
                bom_id = bom_obj.search([('sale_line_id', '=', order_line.id)])
                if bom_id:
                    bom_line.project_ids_lins= [x.id for x in bom_id]
                else:
                    bom_line.project_ids_lins= False

    project_ids_lins=fields.One2many('project.task','project_ids_order',compute="_get_child_bom_lines",string="项目完整信息")


    @api.multi
    def action_confirm(self):
        for order in self:
            #order.state = 'sale'
            #order.confirmation_date = fields.Datetime.now()
            data = {'state':'sale','confirmation_date':fields.Datetime.now() }
            order.write(data)
            if self.env['ir.values'].get_default('sale.config.settings', 'auto_done_setting'):
                data['state']='done'
            if self.env.context.get('send_email'):
                self.force_quotation_send()
            order.order_line._action_procurement_create()

        return True

    # 重写新建函数，生成流水号
    def create_sequence(self,vals,):
        """ 创建序列号
        """
        seq = {'name': vals['prefix'], 'implementation': 'no_gap', 'prefix': vals['prefix'], 'padding': 3,
               'number_increment': 1}
        if 'company_id' in vals:
            seq['company_id'] = vals['company_id']
        yseq_id = self.env['ir.sequence'].sudo().search([('name', '=', seq['name'])])
        yflg = 0
        for rec in self.env['ir.sequence'].sudo().browse(yseq_id):
            yflg = 1
            break
        if yflg:
            return self.env['ir.sequence'].sudo().browse(yseq_id[0]).id
        else:
            return self.env['ir.sequence'].sudo().create(seq)

    # 重置创建函数添加一条新数据
    @api.model
    def create(self,vals):
        # users = self.pool.get('res.users').browse(cr, uid, uid, context=context)
        if not 'sequence_id' in vals or not vals['sequence_id']:
            # 如果没有序列号，则新建
            prefix = str(fields.datetime.now().strftime('%Y%m%d'))
            vals.update({'prefix': prefix})
            vals.update({'sequence_id': self.create_sequence(vals).id})
        # 获取流水号
        vals['name'] = self.env['ir.sequence'].sudo().get_id(vals['sequence_id'])
        return super(Sale_Orderline, self).create(vals)

    @api.multi
    def write(self, context):
        #当前用户Id
        if self.state != 'sale':
            return super(Sale_Orderline, self).write(context)
        else:

            allowed_fields = ['message_follower_ids','procurement_group_id']
            uid=self.env.uid
            group = self.env.ref('ct_beifu.group_beifu_manager')
            group_uids = group.users.mapped('id')
            if uid in group_uids:
                return super(Sale_Orderline, self).write(context)
            elif len(context) == 1 and context.keys()[0] in allowed_fields:
                return super(Sale_Orderline, self).write(context)
            else:
                raise UserError(_('请注意：\n该订单已签合同，您无权限进行操作，请联系管理员!.'))






class sale_order_line(models.Model):
    _inherit = "sale.order.line"
    brand= fields.Char(string="品牌")
    maint_date = fields.Date(string="维保年限")


class ProjectTask(models.Model):
    _inherit = "project.task"
    engin_supervision= fields.Char(string="工程监理")
    positi_time = fields.Datetime(string="定位时间")
    day=fields.Char(string="预计安装天数")
    end_moneny=fields.Selection([
        ('NO',u'未收尾款'),
        ('YES', u'已收尾款')
    ], string="尾款", default="NO")

    invoice_time=fields.Datetime(string="开票时间")
    pay_dection=fields.Char(string="收款情况")
    end_date=fields.Date(string="实际竣工时间")
    work_partner=fields.Char(string="施工队")
    finsh_money=fields.Float(string="施工款")
    project_ids_order=fields.Many2one('sale.order','project_ids_lins')

    def end_obj(self):
        self.stage_id=self.stage_id.id+1

    @api.onchange('end_moneny')
    def on_change_invoice_time(self):
        if self.end_moneny in ['YES']:
            raise UserError(_('请注意：\n是否已确认收款.'))


    # 重置创建函数添加一条新数据
    @api.model
    def create(self,vals):
        street = self.env['res.partner'].browse(int(vals['partner_id']))
        name=vals.get('description')
        # 获取流水号
        vals['name'] =street.street+":"+name
        return super(ProjectTask, self).create(vals)


