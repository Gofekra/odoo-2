# -*- encoding: utf-8 -*-
##############################################################################
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see http://www.gnu.org/licenses/.
#
##############################################################################

{
	'name':"进销存报表",
	'author': 'Shanghai Cotong Software Co., Ltd.',
	'website': 'http://www.qitongyun.cn',
	"version":"1.0",
	'depends':['stock'],
	"description":
u"""
进销存报表
===========================
* 进销存报表

模块说明
---------------------------
进销存报表模块
""",
	"category":"stock",
	"installable":True,
	'application':True,
	"data":[
		"security/ir.model.access.csv",
		"models/qunar_report_stock_view.xml"
		],
}