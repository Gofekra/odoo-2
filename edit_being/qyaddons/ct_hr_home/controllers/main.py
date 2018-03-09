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



class HrController(http.Controller):

	@http.route('/hr/staff_ratio', type='json', auth="user")
	def get_staff_ratio(self):
		"""在职员工比例"""
		employee = request.env['hr.employee']
		entrying_num = employee.search_count([('active', '=', True), ('staff_state', '=', u'入职中')])
		Internship_num = employee.search_count([('active', '=', True), ('staff_state', '=', u'实习期')])
		probation_num = employee.search_count([('active', '=', True), ('staff_state', '=', u'试用期')])
		regular_num = employee.search_count([('active', '=', True), ('staff_state', '=', u'正式员工')])

		return {
			'入职中': entrying_num,
			'实习期': Internship_num,
			'试用期': probation_num,
			'正式员工': regular_num,
		}

	@http.route('/hr/staff_three_ratio', type='json', auth="user")
	def get_staff_three_ratio(self):
		"""试用期/实习生/总人数"""
		employee = request.env['hr.employee']
		total_num = employee.search_count([('active', '=', True)])
		Internship_num = employee.search_count([('active', '=', True), ('staff_state', '=', u'实习期')])
		probation_num = employee.search_count([('active', '=', True), ('staff_state', '=', u'试用期')])

		return {
			'试用期': probation_num,
			'实习生': Internship_num,
			'总人数': total_num,
		}

	@http.route('/hr/staff_education', type='json', auth="user")
	def get_staff_education(self):
		"""员工学历比例"""
		employee = request.env['hr.employee']
		junior_middle_school = employee.search_count([('staff_education', '=', u'初中'), ('active', '=', True)])
		high_school = employee.search_count([('staff_education', '=', u'高中/职高/中专'), ('active', '=', True)])
		junior_college = employee.search_count([('staff_education', '=', u'大学专科'), ('active', '=', True)])
		undergraduate = employee.search_count([('staff_education', '=', u'大学本科'), ('active', '=', True)])
		master = employee.search_count([('staff_education', '=', u'硕士'), ('active', '=', True)])
		doctor = employee.search_count([('staff_education', '=', u'博士'), ('active', '=', True)])
		other = employee.search_count([('staff_education', '=', u'其他'), ('active', '=', True)])

		return {
			'初中': junior_middle_school,
			'高中/职高/中专': high_school,
			'大学专科': junior_college,
			'大学本科': undergraduate,
			'硕士': master,
			'博士': doctor,
			'其他': other,
		}

	@http.route('/hr/staff_gender', type='json', auth="user")
	def get_staff_gender(self):
		"""员工性别比例"""
		employee = request.env['hr.employee']
		male_num = employee.search_count([('gender', '=', 'male'), ('active', '=', True)])
		female_num = employee.search_count([('gender', '=', 'female'), ('active', '=', True)])


		return {
			'男性': male_num,
			'女性': female_num
		}

	@http.route('/hr/staff_marital_status', type='json', auth="user")
	def get_staff_marital_status(self):
		"""员工婚姻状况"""
		employee = request.env['hr.employee']
		single_num = employee.search_count([('marital', '=', 'single'), ('active', '=', True)])
		married_num = employee.search_count([('marital', '=', 'married'), ('active', '=', True)])
		widower_num = employee.search_count([('marital', '=', 'widower'), ('active', '=', True)])
		divorced_num = employee.search_count([('marital', '=', 'divorced'), ('active', '=', True)])
		not_fill_num = employee.search_count([('marital', '=', None), ('active', '=', True)])

		return {
			'单身': single_num,
			'已婚': married_num,
			'丧偶': widower_num,
			'离异': divorced_num,
			'未填写': not_fill_num
		}


	@http.route('/hr/staff_status', type='json', auth="user")
	def get_staff_status(self):
		"""新人人数/在职人数/离职人数"""
		employee = request.env['hr.employee']
		time_now = time.strftime('%Y-%m-%d', time.localtime(time.time()))
		now = datetime.date.today()
		date_on = datetime.date.today().replace(day=1)
		new_staff_num = employee.search_count([('active', '=', True), ('staff_state', 'in', ['入职中','实习期','试用期'])])
		total_num = employee.search_count([('active', '=', True)])
		quit_staff_num = employee.search_count([('active', '=', False),
												("leave_date", ">=", date_on), ("leave_date", "<", time_now)])
		return {
			'新人人数': new_staff_num,
			'在职人数': total_num,
			'离职人数': quit_staff_num,
		}

	@http.route('/hr/staff_contract_status', type='json', auth="user")
	def get_staff_contract_status(self):
		"""未签合同/已签合同/合同到期"""
		employee = request.env['hr.employee']
		staff_data = employee.search([('active', '=', True)])
		time_now = time.strftime('%Y-%m-%d', time.localtime(time.time()))
		date_on = datetime.date.today().replace(day=1)
		no_sign_num = 0
		sign_num = 0
		expire_num = 0
		for x in staff_data:
			if not bool(x.contract_id):
				no_sign_num += 1
			else:
				if x.contract_id.date_end:
					if x.contract_id.date_end>=(str(date_on)) and  x.contract_id.date_end<= time_now:
					  expire_num += 1
				sign_num += 1
		return {
			'未签合同': no_sign_num,
			'已签合同': sign_num,
			'合同到期': expire_num,
		}

	@http.route('/hr/staff_birthday', type='json', auth="user")
	def get_staff_birthday(self):
		"""员工生日列表"""
		employee = request.env['hr.employee']
		staff = employee.search([('active', '=', True)])
		staff_birthday = []
		for x in staff:
			staff_birthday.append(x.birthday)
		return staff_birthday

	@http.route('/payroll/department_month_average_wages', type='json', auth='user')
	def get_department_month_average_wages(self):
		"""部门平均工资"""
		hr_department = request.env['hr.department']
		department_wages_json = []
		now = datetime.date.today()
		month_from, month_to = month_get(now)
		hr_department_data = hr_department.search([
			('active', '=', True),
			('is_add_index', '=', True),
		])
		for department in hr_department_data:
			department_num = self.get_department_member_num(department, True)
			department_wages = self.get_department_wages(month_from, month_to, department, True)
			department_wages_json.append({
				'name': department.name,
				'value': (round(department_wages/department_num, 2) if department_num else 0)
			})
		return department_wages_json	

	def get_department_wages(self, month_from, month_to, department , is_count=False):
		"""
		参数： 一个月的第一天，最后一天，部门，是否计算下级部门总工资
		返回： 某部门的某月总工资
		"""
		department_list = self.get_department_children(department)
		this_department_wages = 0
		for member in department.member_ids:
			this_department_wages += self.get_employee_wages(month_from, month_to, member)
		if is_count:
			total_member_wages = 0
			for department in department_list:
				for member in department.member_ids:
					total_member_wages += self.get_employee_wages(month_from, month_to, member)
			return total_member_wages + this_department_wages
		else:
			return this_department_wages

	def get_department_member_num(self, department, is_count=False):
		"""
		参数： 部门，是否计算下级部门的人数
		返回： 部门总人数
		"""

		employee_num = 0
		if is_count:
			department_list = self.get_department_children(department)
			department_list.append(department)
			for department in department_list:
				employee_num += len(department.member_ids)
		else:
			employee_num = len(department.member_ids)
		return employee_num

	def get_employee_wages(self, month_from, month_to, employee):
		"""
		参数： 一个月的第一天，最后一天，员工
		返回： 员工某月的工资
		"""
		hr_payslip = request.env['hr.payslip']
		hr_payslip_data = hr_payslip.search([('state', '=', 'done'),('date_from', '=', month_from),
			('date_to', '=', month_to),('employee_id', '=', employee.id),
		])
		if hr_payslip_data:
			for wages in hr_payslip_data[0].line_ids:
				if wages.code == 'NET':
					return wages.total
		return 0

	def get_department_children(self, department):
		"""
		参数：部门
		返回：某部门的所有子部门
		"""
		parent_nodes = []
		for x in department.child_ids:
			parent_nodes.append(x)
		sub_nodes = []
		temp_pnodes = []
		while True:
			parent_nodes.extend(temp_pnodes)
			temp_pnodes = []
			for pnode in parent_nodes:
				sub_nodes.append(pnode)
				for sub_node in pnode.child_ids:
					sub_nodes.append(sub_node)
					if sub_node.child_ids:
						temp_pnodes.append(sub_node)
			parent_nodes = []
			if len(temp_pnodes) == 0:
				break				
		return sub_nodes

	def get_total_wages(self, month_from, month_to, is_return=False):
		"""
		参数：一个月的第一天，最后一天，是否返回
		返回：某月的总工资
		"""
		hr_payslip = request.env['hr.payslip']
		hr_payslip_data = hr_payslip.search([
			('state', '=', 'done'),
			('date_from', '=', month_from),
			('date_to', '=', month_to),
		])
		if is_return:
			return len(hr_payslip_data)
		else:
			total_wages = 0
			for x in hr_payslip_data:
				for wages in x.line_ids:
					if wages.code == 'NET':
						total_wages += wages.total
			return total_wages

	@http.route('/hr/staff_department_num', type='json', auth="user")
	def get_staff_department_num(self):
		"""部门人数统计"""
		employee = request.env['hr.employee']
		department = request.env['hr.department']
		department_list = department.search([
			('active', '=', True), 
			('is_add_index', '=', True),
		])
		department_num_json = []
		for department in department_list:
			department_member_num = self.get_department_member_num(department, department.is_census_subordinate)
			department_num_json.append({
				'name': department.name,
				'value': department_member_num
			})

		return department_num_json

