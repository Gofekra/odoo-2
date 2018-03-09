# coding: utf-8
from odoo import models, _
from odoo.exceptions import UserError


class Base(models.AbstractModel):
    _inherit = 'base'

    def _extract_records(self, fields, data, log=lambda a: None, ):
        gen = super(Base, self)._extract_records(fields, data, log)
        oe_import_by_number = self.env.context.get('oe_import_by_number', None)
        if oe_import_by_number:
            by_models = False
            by_fields = []
            params = []
            model_id = self.env['ir.model'].sudo().search([('model', '=', self._name)])
            by_models = self.env['zx.base.import'].sudo().search([('name', '=', model_id.id)])
            if by_models:
                for recordes in by_models.fields:
                    by_fields.append(recordes.name)
            if by_models and by_fields:
                try:
                    params = [(name, fields.index([name])) for name in by_fields]
                except ValueError:
                    res = self.env['ir.model.fields'].sudo().search(
                        [('model', '=', self._name), ('name', '=', name)])
                    log({'type': 'error', 'message': u' 导入文件中缺少必需字段\n:%s' % res.field_description})
            for record, extras in gen:
                if not by_models or not params:
                    yield record, extras
                else:
                    domain = [(name, '=', data[extras['rows']['from']][idx]) for name, idx in params]
                    db_id = self.search(domain).ids
                    if len(db_id) == 1:
                        record['.id'] = db_id[0]
                    elif len(db_id) > 1:
                        log({'type': 'error', 'message': u'满足选定字段组合查询的数据超过一条, 无法实现更新\n%s' % domain})
                    yield record, extras
        else:
            for record, extras in gen:
                yield record, extras
