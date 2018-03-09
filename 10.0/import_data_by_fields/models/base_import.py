# coding: utf-8
import logging
import psycopg2

from odoo import models, api

_logger = logging.getLogger(__name__)


class Import(models.TransientModel):
    _inherit = 'base_import.import'

    @api.multi
    def do(self, fields, options, dryrun=False):
        print options
        if options.get('oe_import_by_number'):
            self = self.with_context(oe_import_by_number=True)
        return super(Import, self).do(fields, options, dryrun=dryrun)
