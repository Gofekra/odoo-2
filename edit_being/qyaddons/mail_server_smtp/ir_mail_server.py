# -*- coding: utf-8 -*-
from odoo import SUPERUSER_ID
from odoo.osv import osv
import odoo.tools as tools


class ir_mail_server(osv.osv):
    _inherit = "ir.mail_server"

    def send_email(self, message, mail_server_id=None, smtp_server=None, smtp_port=None,
                   smtp_user=None, smtp_password=None, smtp_encryption=None, smtp_debug=False,
                   context=None):
        # Get SMTP Server Details from Mail Server
        mail_server = None
        if mail_server_id:
            mail_server = self.browse( mail_server_id)
        elif not smtp_server:
            #print SUPERUSER_ID
            mail_server_ids = self.search([], order='sequence', limit=1)
            #if mail_server_ids:
            mail_server = mail_server_ids[0]

        if mail_server:
            smtp_server = mail_server.smtp_host
            smtp_user = mail_server.smtp_user
            smtp_password = mail_server.smtp_pass
            smtp_port = mail_server.smtp_port
            smtp_encryption = mail_server.smtp_encryption
            smtp_debug = smtp_debug or mail_server.smtp_debug
        else:
            # we were passed an explicit smtp_server or nothing at all
            smtp_server = smtp_server or tools.config.get('smtp_server')
            smtp_port = tools.config.get('smtp_port', 25) if smtp_port is None else smtp_port
            smtp_user = smtp_user or tools.config.get('smtp_user')
            smtp_password = smtp_password or tools.config.get('smtp_password')
            if smtp_encryption is None and tools.config.get('smtp_ssl'):
                smtp_encryption = 'starttls' # STARTTLS is the new meaning of the smtp_ssl flag as of v7.0
        message.replace_header('From', '%s <%s>' % (message['From'], smtp_user))
        if message.has_key('return-path'):
            message.replace_header('return-path', '%s' % (smtp_user,))
        else:
            message.add_header('return-path', '%s' % (smtp_user,))

        return super(ir_mail_server, self).send_email( message, mail_server_id=None, smtp_server=None, smtp_port=None,
                   smtp_user=None, smtp_password=None, smtp_encryption=None, smtp_debug=False)
