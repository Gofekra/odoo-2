# coding: utf-8


from odoo import api
from odoo.modules.registry import Registry
from odoo import http, SUPERUSER_ID, exceptions, _
from odoo.http import request

from odoo.addons.web.controllers.main import Home, ensure_db


class LoginCtr(Home):
    @http.route()
    def web_login(self, redirect=None, **kw):
        ensure_db()
        request.params['login_success'] = False
        if request.httprequest.method == 'GET' and redirect and request.session.uid:
            return http.redirect_with_hash(redirect)

        if not request.uid:
            request.uid = SUPERUSER_ID
        values = request.params.copy()
        try:
            values['databases'] = http.db_list()
        except exceptions.AccessDenied:
            values['databases'] = None

        # 只特殊处理post的情况
        if request.httprequest.method == 'POST':
            registry = Registry(request.session.db)
            with registry.cursor() as cr:
                env = api.Environment(cr, 1, {})
                login_user = env['res.users'].search([('login', '=', request.params['login'])])
                time_limit = int(env['ir.config_parameter'].get_param('auth_time_limit.login_error_times'))

                # 9次失败之后，不再后台验证密码，直接返回
                if login_user and login_user.login_error_times >= time_limit:
                    values['error'] = u'账户已被锁定!'
                    return request.render('web.login', values)

                old_uid = request.uid
                uid = request.session.authenticate(request.session.db, request.params['login'], request.params['password'])

                # 登录成功
                if uid is not False:
                    login_user.login_error_times = 0
                    request.params['login_success'] = True
                    if not redirect:
                        redirect = '/web'
                    return http.redirect_with_hash(redirect)

                # 登录失败
                request.uid = old_uid
                if login_user.exists():
                    try:
                        login_user.sudo(login_user.id).check_credentials(request.params['password'])
                    except exceptions.AccessDenied:
                        # 密码错误
                        login_user.login_error_times += 1
                        if login_user.login_error_times == time_limit:
                            values['error'] = u'账户已被锁定!'
                        elif login_user.login_error_times >= time_limit - 3:
                            values['error'] = u"您还有%s次机会！" % (time_limit - login_user.login_error_times)
                        else:
                            values['error'] = _("Wrong login/password")
                    else:
                        # 密码正确, 其他验证失败, allowed_ips
                        values['error'] = u'访问受限，请与管理员联系。'
                else:
                    # 无此用户, 或者此用户active = False
                    values['error'] = u"无此用户"

        return request.render('web.login', values)
