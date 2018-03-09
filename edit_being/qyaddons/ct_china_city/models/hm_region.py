#coding:utf-8

from odoo import fields,models
import base64
try:
    import xlrd
    try:
        from xlrd import xlsx
    except ImportError:
        xlsx = None
except ImportError:
    xlrd = xlsx = None

class hm_region(models.Model):
		_name="hm.region"


		xls=fields.Binary('XLS File')


		def btn_import(self):
			for wiz in self:
				if not wiz.xls:
						continue
				excel = xlrd.open_workbook(file_contents=base64.decodestring(wiz.xls))
				sheets=excel.sheets()
				for sh in sheets:
					for row in range(1,sh.nrows):
						state = sh.cell(row,0).value
						city = sh.cell(row,1).value
						district = sh.cell(row,2).value

						#read state
						states = self.env['res.country.state'].search([('name','=',state)])
						if states:
							cities = self.env['hm.city'].search([('name','=',city)])
							if len(cities):
								dises = self.env['hm.district'].search([('name','=',district)])
								if dises:
										continue
								else:
									self.env['hm.district'].create({'name':district,'city':cities.id})
							else:
								c_id=self.env['hm.city'].create({'name':city,'state':states.id})

								self.env['hm.district'].create({'name':district,'city':c_id.id})
					else:
							model,china = self.env['ir.model.data'].get_object_reference('base','cn')
							print china
							if china:
								s_id = self.env['res.country.state'].create({'name':state,'country_id':china,'code':'0'})
								c_id=self.env['hm.city'].create({'name':city,'state':s_id.id})
								self.env['hm.district'].create({'name':district,'city':c_id.id})
							else:
								ch_id = self.env['res.country'].create({'name':'China'})
								cty_id=ch_id
								s_id = self.env['res.country.state'].create({'name':state,'country_id':ch_id,'code':'0'})
								c_id=self.env['hm.city'].create({'name':city,'state':s_id.id})
								self.env['hm.district'].create({'name':district,'city':c_id.id})
											
																
							
