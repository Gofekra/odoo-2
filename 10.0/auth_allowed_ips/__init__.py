# coding: utf-8

import re
import logging
from odoo import models, fields, SUPERUSER_ID, api

_logger = logging.getLogger(__name__)


class User(models.Model):
    _inherit = 'res.users'

    allowed_ips = fields.Text(string='Allowed IPs', help=u"""正则匹配
    如：^192\.168\.2\.\d{1,3}$， 支持多个正则，每一个正则单独一行。满足任意一行即可通过。
""")

    @classmethod
    def authenticate(cls, db, login, password, user_agent_env):
        uid = super(User, cls).authenticate(db, login, password, user_agent_env)
        if uid:
            with cls.pool.cursor() as cr:
                self = api.Environment(cr, SUPERUSER_ID, {})[cls._name]
                user = self.browse(uid)
                if hasattr(user, 'allowed_ips') and user.allowed_ips:
                    addr = user_agent_env['REMOTE_ADDR']
                    if not any(re.match(line, addr) for line in user.allowed_ips.splitlines()):
                        _logger.warn('User login blocked cause of the remote_addr %s not match allowed_ips %s',
                                     user_agent_env['REMOTE_ADDR'], user.allowed_ips)
                        uid = False

                        # 在super方法中，已经普通密码验证成功，且创建了登录成功的日志，
                        # 但是在上面被IP限制，修改此login最后一条的日志和note。
                        Log = api.Environment(cr, SUPERUSER_ID, {})['auth_login_log.log']
                        Log.search([('login_account', '=', login)], limit=1, order='id desc').write({
                            'note': u'IP受限',
                            'login_status': 'e',
                        })

        return uid
