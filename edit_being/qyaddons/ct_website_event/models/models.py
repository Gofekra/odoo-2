# -*- coding: utf-8 -*-
from  odoo import modules, models, fields, api,tools
import datetime
import urllib,urllib2
import re,cookielib
import logging
from odoo.http import request
_logger = logging.getLogger(__name__)

class back_user(models.Model):
    _name = 'back.user'

    name=fields.Many2one('event.event',string="活动")
    user_id = fields.Many2one('res.users', string="姓名")
    ip = fields.Char(string="IP")
    type = fields.Char(string="来源")
    date = fields.Datetime(string="访问时间")


class EventRegistration(models.Model):
    _inherit = 'event.registration'

    user_id = fields.Many2one('res.users', string="推荐人")


    @api.model
    def _prepare_attendee_values(self, registration):

        cookie_content = request.httprequest.cookies.get('inherit_id') or ''
        """ Override to add sale related stuff """
        line_id = registration.get('sale_order_line_id')
        if line_id:
            registration.setdefault('partner_id', line_id.order_id.partner_id)
        att_data = super(EventRegistration, self)._prepare_attendee_values(registration)
        if line_id:
            att_data.update({
                'event_id': line_id.event_id.id,
                'event_ticket_id': line_id.event_ticket_id.id,
                'origin': line_id.order_id.name,
                'sale_order_id': line_id.order_id.id,
                'sale_order_line_id': line_id.id,
                'user_id':cookie_content
            })
        return att_data


class EventUserReport(models.Model):
    _name = "event.user.report"
    _auto = False
    name=fields.Many2one('event.event',string="活动")
    user_id = fields.Many2one('res.users', string="姓名")
    cqty=fields.Integer(string="访问数")
    dqty=fields.Integer(string="登记数")
    qty=fields.Float(string="转化率")

    @api.model_cr
    def init(self):
        tools.drop_view_if_exists(self._cr, 'event_user_report')
        self._cr.execute("""
            create view event_user_report as (                                         
                		select Row_Number() over ( ) as id ,ta.name,ta.user_id,cqty,dqty,CASE WHEN cqty=0 THEN cqty ELSE  round(dqty::numeric/cqty::numeric,2) END   as qty from (
                        select user_id,name,count(user_id) as cqty FROM public.back_user  group by user_id,name
                    
                        ) as ta 
                    
                      left join (
                    
                        SELECT user_id,event_id,count(user_id) as dqty FROM public.event_registration  group by user_id,event_id
                        )
                     as tb on ta.user_id=tb.user_id and ta.name=tb.event_id

            )
            """)

