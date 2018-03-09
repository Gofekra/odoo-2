# -*- encoding: utf-8 -*-
###############################################################################
# overright fields_view_get of BaseModel for getting  certain views to certain users
###############################################################################

from odoo.osv.orm import BaseModel
from odoo import models, fields, api, _
import babel.dates
import calendar
import collections
import copy
import datetime
import itertools
import logging
import operator
import pickle
import re
import simplejson
import time
import traceback
import types
import psycopg2
from lxml import etree

import odoo
import odoo.netsvc as netsvc
import odoo.tools as tools
from odoo.tools.config import config
from odoo.tools.misc import CountingStream
from odoo.tools.safe_eval import safe_eval as eval
from odoo.tools.translate import _
from odoo import SUPERUSER_ID
from odoo.exceptions import except_orm

from odoo.tools import SKIPPED_ELEMENT_TYPES

class BaseModelExtend(models.AbstractModel):
    _name = 'basemodel.extend'

    def _register_hook(self):

        # @api.cr_uid_context
        @api.model
        def fields_view_get(self, view_id=None, view_type='form',  toolbar=False, submenu=False):
            context = {}
            def encode(s):
                if isinstance(s, unicode):
                    return s.encode('utf8')
                return s

            def raise_view_error(error_msg, child_view_id):
                view, child_view = self.env['ir.ui.view'].browse([view_id, child_view_id])
                error_msg = error_msg % {'parent_xml_id': view.xml_id}
                raise AttributeError("View definition error for inherited view '%s' on model '%s': %s"
                                     % (child_view.xml_id, self._name, error_msg))

            def locate(source, spec):

                if spec.tag == 'xpath':
                    nodes = source.xpath(spec.get('expr'))
                    return nodes[0] if nodes else None
                elif spec.tag == 'field':
                    for node in source.getiterator('field'):
                        if node.get('name') == spec.get('name'):
                            return node
                    return None

                for node in source.getiterator(spec.tag):
                    if isinstance(node, SKIPPED_ELEMENT_TYPES):
                        continue
                    if all(node.get(attr) == spec.get(attr) \
                           for attr in spec.attrib
                           if attr not in ('position', 'version')):
                        # Version spec should match parent's root element's version
                        if spec.get('version') and spec.get('version') != source.get('version'):
                            return None
                        return node
                return None

            def apply_inheritance_specs(source, specs_arch, inherit_id=None):

                specs_tree = etree.fromstring(encode(specs_arch))
                specs = [specs_tree]

                while len(specs):
                    spec = specs.pop(0)
                    if isinstance(spec, SKIPPED_ELEMENT_TYPES):
                        continue
                    if spec.tag == 'data':
                        specs += [c for c in specs_tree]
                        continue
                    node = locate(source, spec)
                    if node is not None:
                        pos = spec.get('position', 'inside')
                        if pos == 'replace':
                            if node.getparent() is None:
                                source = copy.deepcopy(spec[0])
                            else:
                                for child in spec:
                                    node.addprevious(child)
                                node.getparent().remove(node)
                        elif pos == 'attributes':
                            for child in spec.getiterator('attribute'):
                                # attribute =None# (child.get('name'), child.text and child.text.encode('utf8') or None)
                                # if attribute[1]:
                                #     node.set(attribute[0], attribute[1])
                                # else:
                                #     del (node.attrib[attribute[0]])
                                attribute = child.get('name')
                                value = child.text or ''
                                if child.get('add') or child.get('remove'):
                                    assert not child.text
                                    separator = child.get('separator', ',')
                                    if separator == ' ':
                                        separator = None  # squash spaces
                                    to_add = filter(bool, map(str.strip, child.get('add', '').split(separator)))
                                    to_remove = map(str.strip, child.get('remove', '').split(separator))
                                    values = map(str.strip, node.get(attribute, '').split(separator))
                                    value = (separator or ' ').join(
                                        filter(lambda s: s not in to_remove, values) + to_add)
                                if value:
                                    node.set(attribute, value)
                                elif attribute in node.attrib:
                                    del node.attrib[attribute]
                        else:
                            sib = node.getnext()
                            for child in spec:
                                if pos == 'inside':
                                    node.append(child)
                                elif pos == 'after':
                                    if sib is None:
                                        node.addnext(child)
                                        node = child
                                    else:
                                        sib.addprevious(child)
                                elif pos == 'before':
                                    node.addprevious(child)
                                else:
                                    raise_view_error("Invalid position value: '%s'" % pos, inherit_id)
                    else:
                        attrs = ''.join([
                            ' %s="%s"' % (attr, spec.get(attr))
                            for attr in spec.attrib
                            if attr != 'position'
                        ])
                        tag = "<%s%s>" % (spec.tag, attrs)
                        if spec.get('version') and spec.get('version') != source.get('version'):
                            raise_view_error(
                                "Mismatching view API version for element '%s': %r vs %r in parent view '%%(parent_xml_id)s'" % \
                                (tag, spec.get('version'), source.get('version')), inherit_id)
                        raise_view_error("Element '%s' not found in parent view '%%(parent_xml_id)s'" % tag, inherit_id)
                return source

            def apply_view_inheritance( source, inherit_id):
                """ Apply all the (directly and indirectly) inheriting views.

                :param source: a parent architecture to modify (with parent
                    modifications already applied)
                :param inherit_id: the database view_id of the parent view
                :return: a modified source where all the modifying architecture
                    are applied

                """
                sql_inherit = self.env['ir.ui.view'].get_inheriting_views_arch( inherit_id, self._name,)
                for (view_arch, view_id) in sql_inherit:
                    source = apply_inheritance_specs(source, view_arch, view_id)
                    source = apply_view_inheritance( source, view_id)
                return source

            result = {'type': view_type, 'model': self._name}

            sql_res = False
            parent_view_model = None
            view_ref = context.get(view_type + '_view_ref')
            # Search for a root (i.e. without any parent) view.
            while True:
                if view_ref and not view_id:
                    if '.' in view_ref:
                        module, view_ref = view_ref.split('.', 1)
                        self.env.cr.execute(
                            "SELECT res_id FROM ir_model_data WHERE model='ir.ui.view' AND module=%s AND name=%s",
                            (module, view_ref))
                        view_ref_res = self.env.cr.fetchone()
                        if view_ref_res:
                            view_id = view_ref_res[0]
                check_c_tree_id = self.env['ir.module.module'].search( [('name', '=', 'ct_treeview'),('state', '=', 'installed')])

                # self.env.cr.execute("""SELECT *  FROM ir_module_module  WHERE name='ct_treeview' and  state='installed' """)
                # check_c_tree_id = self.env.cr.fetchone()

                if check_c_tree_id:
                    if view_id:
                        if view_type == 'tree':
                            self.env.cr.execute("""SELECT arch_db,name,field_parent,id,type,inherit_id,model
                                          FROM ir_ui_view
                                          WHERE id=%s and customized_for=%s and type=%s and default_view1=%s AND customized_view=%s""",
                                       (view_id, self.env.uid, 'tree', False, True))
                            sql_res = self.env.cr.dictfetchone()
                            if not sql_res:
                                self.env.cr.execute("""SELECT arch_db,name,field_parent,id,type,inherit_id,model
                                              FROM ir_ui_view
                                              WHERE model=%s AND customized_for=%s and type=%s and default_view1=%s AND customized_view=%s""",
                                           (self._name, self.env.uid, 'tree', False, True))
                                sql_res = self.env.cr.dictfetchone()
                                if not sql_res:
                                    self.env.cr.execute("""SELECT arch_db,name,field_parent,id,type,inherit_id,model
                                                  FROM ir_ui_view
                                                  WHERE id=%s""", (view_id,))
                        else:
                            self.env.cr.execute("""SELECT arch_db,name,field_parent,id,type,inherit_id,model
                                          FROM ir_ui_view
                                          WHERE id=%s""", (view_id,))
                            sql_res = self.env.cr.dictfetchone()
                    else:
                        if view_type == 'tree':
                            self.env.cr.execute("""SELECT arch_db,name,field_parent,id,type,inherit_id,model
                                          FROM ir_ui_view
                                          WHERE model=%s AND type=%s AND customized_for=%s AND default_view1=%s AND customized_view=%s 
                                          ORDER BY priority""", (self._name, 'tree', self.env.uid, False, True))
                            sql_res = self.env.cr.dictfetchone()
                            if not sql_res:
                                self.env.cr.execute("""SELECT arch_db,name,field_parent,id,type,inherit_id,model
                                              FROM ir_ui_view
                                              WHERE model=%s AND type=%s AND default_view1=%s AND customized_view is NULL
                                              ORDER BY priority""", (self._name, view_type, True))
                        else:
                            self.env.cr.execute("""SELECT arch_db,name,field_parent,id,type,inherit_id,model
                                          FROM ir_ui_view
                                          WHERE model=%s AND type=%s AND inherit_id IS NULL
                                          ORDER BY priority""", (self._name, view_type))
                else:
                    if view_id:
                        self.env.cr.execute("""SELECT arch_db,name,field_parent,id,type,inherit_id,model
                                      FROM ir_ui_view
                                      WHERE id=%s""", (view_id,))
                    else:
                        self.env.cr.execute("""SELECT arch_db,name,field_parent,id,type,inherit_id,model
                                      FROM ir_ui_view
                                      WHERE model=%s AND type=%s AND inherit_id IS NULL
                                      ORDER BY priority""", (self._name, view_type))

                if not sql_res:
                    sql_res = self.env.cr.dictfetchone()
                    if not sql_res:
                        break

                view_id = sql_res['inherit_id'] or sql_res['id']
                parent_view_model = sql_res['model']
                if not sql_res['inherit_id']:
                    break

            # if a view was found
            if sql_res:
                source = etree.fromstring(encode(sql_res['arch_db']))
                result.update(
                    arch=apply_view_inheritance( source, sql_res['id']),
                    type=sql_res['type'],
                    view_id=sql_res['id'],
                    name=sql_res['name'],
                    field_parent=sql_res['field_parent'] or False)
            else:
                # otherwise, build some kind of default view
                try:
                    view = getattr(self, '_get_default_%s_view' % view_type)()
                except AttributeError:
                    # what happens here, graph case?
                    raise except_orm(_('Invalid Architecture!'),
                                     _("There is no view of type '%s' defined for the structure!") % view_type)

                result.update(
                    arch=view,
                    name='default',
                    field_parent=False,
                    view_id=0)
            if parent_view_model != BaseModel._name:
                ctx = context.copy()
                ctx['base_model_name'] = parent_view_model
            else:
                ctx = context
            xarch, xfields=self.env['ir.ui.view'].postprocess_and_fields( self._name, result['arch'], view_id)
            result['arch'] = xarch
            result['fields'] = xfields
            if toolbar:
                def clean(x):
                    x = x[2]
                    for key in ('report_sxw_content', 'report_rml_content',
                                'report_sxw', 'report_rml',
                                'report_sxw_content_data', 'report_rml_content_data'):
                        if key in x:
                            del x[key]
                    return x

                IrValues = self.env['ir.values']
                resprint = IrValues.get_actions('client_print_multi', self._name)
                resaction = IrValues.get_actions('client_action_multi', self._name)
                resrelate = IrValues.get_actions('client_action_relate', self._name)
                resprint = [clean(print_)
                            for print_ in resprint
                            if view_type == 'tree' or not print_[2].get('multi')]
                resaction = [clean(action)
                             for action in resaction
                             if view_type == 'tree' or not action[2].get('multi')]
                # When multi="True" set it will display only in More of the list view
                resrelate = [clean(action)
                             for action in resrelate
                             if (action[2].get('multi') and view_type == 'tree') or (
                             not action[2].get('multi') and view_type == 'form')]

                for x in itertools.chain(resprint, resaction, resrelate):
                    x['string'] = x['name']

                result['toolbar'] = {
                    'print': resprint,
                    'action': resaction,
                    'relate': resrelate
                }
            return result

        @api.model
        def _generate_order_by_inner(self, alias, order_spec, query, reverse_direction=False, seen=None):

            if seen is None:
                seen = set()
            self._check_qorder(order_spec)

            order_by_elements = []
            for order_part in order_spec.split(','):
                order_split = order_part.strip().split(' ')
                order_field = order_split[0].strip()
                order_direction = order_split[1].strip().upper() if len(order_split) == 2 else ''
                if reverse_direction:
                    order_direction = 'ASC' if order_direction == 'DESC' else 'DESC'
                do_reverse = order_direction == 'DESC'
                field = self._fields.get(order_field)
                if not field:
                    raise ValueError(_("Sorting field %s not found on model %s") % (order_field, self._name))

                if order_field == 'id':
                    order_by_elements.append('"%s"."%s" %s' % (alias, order_field, order_direction))
                else:
                    if field.inherited:
                        field = field.base_field
                    if field.store and field.type == 'many2one':
                        key = (field.model_name, field.comodel_name, order_field)
                        if key not in seen:
                            seen.add(key)
                            order_by_elements += self._generate_m2o_order_by(alias, order_field, query, do_reverse,
                                                                             seen)
                    elif field.store and field.column_type:
                        qualifield_name = self._inherits_join_calc(alias, order_field, query, implicit=False,
                                                                   outer=True)
                        if field.type == 'boolean':
                            qualifield_name = "COALESCE(%s, false)" % qualifield_name
                        order_by_elements.append("%s %s" % (qualifield_name, order_direction))
                    else:
                        continue  # ignore non-readable or "non-joinable" fields

            return order_by_elements

        models.BaseModel.fields_view_get = fields_view_get
        models.BaseModel._generate_order_by_inner = _generate_order_by_inner
        return super(BaseModelExtend, self)._register_hook()

