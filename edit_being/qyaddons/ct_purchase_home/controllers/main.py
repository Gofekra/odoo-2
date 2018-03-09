# -*- coding: utf-8 -*-
import time
import datetime

from odoo import http
from odoo.http import request


def month_get(d):
    """
    参数：datetime.date
    返回上个月第一个天和最后一天的日期时间
    :return
    date_from: 2016-01-01
    date_to: 2016-01-31
    """
    dayscount = datetime.timedelta(days=d.day)
    dayto = d - dayscount
    date_from = datetime.date(dayto.year, dayto.month, 1)
    date_to = datetime.date(dayto.year, dayto.month, dayto.day)
    return date_from, date_to


class PurchaseController(http.Controller):

	@http.route('/purchase/order_planned', type='json', auth="user")
	def get_order_planned(self):
		"""采购到货情况预测"""
		order_warns = []
		now = datetime.datetime.now()
		now_5 = now + datetime.timedelta(days=5)
		now_5.strftime('%Y-%m-%d %H:%M:%S')
		now.strftime('%Y-%m-%d %H:%M:%S')
		purchase_order = request.env['purchase.order']

		uid=request.env.uid  #当前用户id
		user = request.env.user #当前用户
		if user.has_group('purchase.group_purchase_manager'): #权限组--采购经理
			order_data = purchase_order.search([('date_planned', '<', str(now_5)), 
			('date_planned', '>', str(now)),
			('state', 'in' ,['purchase', 'done']),
			])
		else:
			order_data = purchase_order.search([('date_planned', '<', str(now_5)), 
				('date_planned', '>', str(now)),
				('state', 'in' ,['purchase', 'done']),
				('create_uid', '=' ,uid),
				])
		if order_data:
			for x in order_data:
				order_warns.append({
					'采购单号': x.name,
					'供应商': x.partner_id.name,
					'交货日期': x.date_planned[0:11],
					'id': x.id,
				    'model_name': 'purchase.order',
				})

		return order_warns

	@http.route('/purchase/product_num_top', type='json', auth="user")
	def get_product_num_top(self):
		"""采购数量TOP5"""
		product_product = request.env['product.product']
		stock_move = request.env['stock.move']

		uid=request.env.uid  #当前用户id
		user = request.env.user #当前用户
		product_data = product_product.search([('purchase_ok', '=', 1), ('active', '=', True)])
		#找到所有可被采购的产品
		product_top = {}
		now = datetime.date.today()
		month_from, month_to = month_get(now)
		to = month_to + datetime.timedelta(days=1)
		month_from, month_to = month_get(month_from)
		month_from, month_to = month_get(month_from)

		for x in product_data:
			if user.has_group('purchase.group_purchase_manager'): #权限组--采购经理
				stocks = stock_move.search([
					('product_id', '=', x.id),
					('create_date', '<=', time.strftime("%Y-%m-%d %H:%M:%S", to.timetuple())),
					('create_date', '>=', time.strftime("%Y-%m-%d %H:%M:%S", month_from.timetuple())),
				])
			else:
				stocks = stock_move.search([
					('create_uid', '=', uid),
					('product_id', '=', x.id),
					('create_date', '<=', time.strftime("%Y-%m-%d %H:%M:%S", to.timetuple())),
					('create_date', '>=', time.strftime("%Y-%m-%d %H:%M:%S", month_from.timetuple())),
				])
			purchase_product_num = 0
			if stocks:
				for stock in stocks:
					purchase_product_num += stock.product_uom_qty
			product_top[x.name] = purchase_product_num
		product_top = sorted(product_top.items(), key=lambda item:item[1], reverse=True)
		product_top_len = len(product_top)
		if product_top_len > 5:
			product_top = product_top[0:5]
		product_top = dict(product_top)
		return product_top

	@http.route('/purchase/product_value_top', type='json', auth="user")
	def get_product_value_top(self):
		"""采购金额TOP5"""
		product_product = request.env['product.product']
		purchase_order = request.env['purchase.order']
		now = datetime.date.today()
		month_from, month_to = month_get(now)
		to = month_to + datetime.timedelta(days=1)
		month_from, month_to = month_get(month_from)
		month_from, month_to = month_get(month_from)

		uid=request.env.uid  #当前用户id
		user = request.env.user #当前用户
		if user.has_group('purchase.group_purchase_manager'): #权限组--采购经理
			purchase_order_data = purchase_order.search([
				('state', 'in', ['purchase', 'done']),
				('date_order', '<=', time.strftime("%Y-%m-%d %H:%M:%S", to.timetuple())),
				('date_order', '>=', time.strftime("%Y-%m-%d %H:%M:%S", month_from.timetuple())),
			])
			product_data = product_product.search([
				('active', '=', True),
			])
		else:
			purchase_order_data = purchase_order.search([
				('state', 'in', ['purchase', 'done']),
				('create_uid', '=' ,uid),
				('date_order', '<=', time.strftime("%Y-%m-%d %H:%M:%S", to.timetuple())),
				('date_order', '>=', time.strftime("%Y-%m-%d %H:%M:%S", month_from.timetuple())),
			])
			product_data = product_product.search([
				('active', '=', True),
			])

		top_5 = {}
		for product in product_data:
			top_5[product.name] = 0
		for purchase_order in purchase_order_data:
			for product_1 in purchase_order.order_line:
				for product_2 in product_data:
					if product_1.product_id == product_2:
						top_5[product_2.name] = top_5[product_2.name] + product_1.price_subtotal
		top_5 = sorted(top_5.items(), key=lambda item:item[1], reverse=True)
		top_5_len = len(top_5)
		if top_5_len > 5:
			top_5 = top_5[0:5]
		top_5 = dict(top_5)
		return top_5
