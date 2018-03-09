#-*- coding:utf-8 -*-
##############################################################################
#
#    Powered By Rainsoft(QingDao) Author:Kevin Kong 2014 (kfx2007@163.com)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
{
		"name":u"china city",
		"category": "Generic Modules/Others",
		"version":"1.0",
		"description":u"""
China City
================================================================
先使用命令：pip install xlrd
China City model is created for customers who are loacated in China main land.
This model changes the format of partner's address,makes it looks much better from chinese's view.
		  """,
		'author': "Shanghai Cotong Software Co., Ltd.",
		'website': "http://www.qitongyun.cn",
		"depends":["base",'sales_team'],
        "data":[
			"views/hm_city_view.xml",
			"views/hm_region_view.xml",
			"views/hm_partner_view.xml",
            "views/res_company_view.xml",
                ],
		"installable":True,

}
