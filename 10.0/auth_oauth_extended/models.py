#-*- coding: utf-8 -*-

from werkzeug.exceptions import BadRequest
import functools
import logging
import simplejson
import urllib2
import urlparse
import urlparse
import werkzeug.urls
import werkzeug.utils

import odoo

from odoo import fields,models,api
from odoo import http
from odoo import SUPERUSER_ID
from odoo.addons.auth_oauth.controllers.main import fragment_to_query_string
from odoo.addons.auth_oauth.controllers.main import OAuthController
from odoo.addons.auth_signup.models.res_partner import SignupError, now

from odoo.addons.web.controllers.main import login_and_redirect
from odoo.addons.web.controllers.main import set_cookie_and_redirect

from odoo.modules.registry import RegistryManager
from odoo.tools.translate import _

_logger = logging.getLogger(__name__)


class OAuthController_extend(OAuthController):

    @http.route('/auth_oauth/signin', type='http', auth='none')
    @fragment_to_query_string
    def signin(self, **kw):
        kw = simplejson.loads(simplejson.dumps(kw).replace('+',''))
        state = simplejson.loads(kw['state'])
        dbname = state['d']
        provider = state['p']
        context = state.get('c', {})
        registry = RegistryManager.get(dbname)
        with registry.cursor() as cr:
            try:
                env = api.Environment(cr, SUPERUSER_ID, context)
                credentials = env['res.users'].sudo().auth_oauth(provider, kw)
                print credentials
                # u = registry.get('res.users')
                # credentials = u.auth_oauth(provider, kw)
                cr.commit()
                action = state.get('a')
                menu = state.get('m')
                redirect = werkzeug.url_unquote_plus(state['r']) if state.get('r') else False
                url = '/web'
                if redirect:
                    url = redirect
                elif action:
                    url = '/web#action=%s' % action
                elif menu:
                    url = '/web#menu_id=%s' % menu
                return login_and_redirect(*credentials, redirect_url=url)
            except AttributeError:
                # auth_signup is not installed
                _logger.error("auth_signup not installed on database %s: oauth sign up cancelled." % (dbname,))
                url = "/web/login?oauth_error=1"
            except odoo.exceptions.AccessDenied:
                # oauth credentials not valid, user could be on a temporary session
                _logger.info('OAuth2: access denied, redirect to main page in case a valid session exists, without setting cookies')
                url = "/web/login?oauth_error=3"
                redirect = werkzeug.utils.redirect(url, 303)
                redirect.autocorrect_location_header = False
                return redirect
            except Exception, e:
                # signup error
                _logger.exception("OAuth2: %s" % str(e))
                url = "/web/login?oauth_error=2"

        return set_cookie_and_redirect(url)

class auth_oauth_provider(models.Model):
    _inherit = 'auth.oauth.provider'

    provider_type = [
        ('qq', 'for QQ'),
        ('weixin', 'for Weixin'),
        ('weibo', 'for Weibo'),
        ('other', 'for Other'),

    ]

    provider_type = fields.Selection(provider_type, 'Provider Type', required=True)

    _defaults = {
        'provider_type': 'other',
    }


class res_users(models.Model):
    _inherit = 'res.users'


    def _auth_oauth_rpc(self,endpoint, access_token):
        params = werkzeug.url_encode({'access_token': access_token})
        if urlparse.urlparse(endpoint)[4]:
            url = endpoint + '&' + params
        else:
            url = endpoint + '?' + params
        f = urllib2.urlopen(url)
        response = f.read()
        if response.find('callback') == 0:
            response = response[response.index("(") + 1: response.rindex(")")]
        return simplejson.loads(response)

    def _auth_oauth_signin(self,provider, validation, params):

        """ retrieve and sign in the user corresponding to provider and validated access token
            :param provider: oauth provider id (int)
            :param validation: result of validation of access token (dict)
            :param params: oauth parameters (dict)
            :return: user login (str)
            :raise: odoo.exceptions.AccessDenied if signin failed

            This method can be overridden to add alternative signin methods.
        """
        try:

            provider_obj = self.env['auth.oauth.provider'].sudo().read(provider)
            provider_type = provider_obj['provider_type']

            if provider_type == 'qq':
                oauth_uid = validation['openid']
            elif provider_type == 'weixin':
                oauth_uid = validation['openid']
            elif provider_type == 'weibo':
                oauth_uid = validation['userid']
            else:
                oauth_uid = validation['user_id']

            user_ids = self.search([("oauth_uid", "=", oauth_uid), ('oauth_provider_id', '=', provider)])
            if not user_ids:
                raise odoo.exceptions.AccessDenied()
            assert len(user_ids) == 1
            user = self.browse(user_ids[0])
            user.write({'oauth_access_token': params['access_token']})
            return user.login
        except odoo.exceptions.AccessDenied, access_denied_exception:
            state = simplejson.loads(params['state'])
            token = state.get('t')
            provider_obj = self.pool['auth.oauth.provider'].read(provider)
            provider_type = provider_obj['provider_type']

            if provider_type == 'qq':
                oauth_uid = validation['nickname']
            elif provider_type == 'weixin':
                oauth_uid = validation['openid']
            elif provider_type == 'weibo':
                oauth_uid = validation['userid']
            else:
                oauth_uid = validation['user_id']
            email = validation.get('email', '%_%s' % (provider_type, oauth_uid))
            name = validation.get('name', email)
            values = {
                'name': name,
                'login': email,
                'email': email,
                'oauth_provider_id': provider,
                'oauth_uid': oauth_uid,
                'oauth_access_token': params['access_token'],
                'active': True,
            }
            _logger.info(values)
            try:
                _, login, _ = self.signup(values, token)
                return login
            except SignupError:
                _logger.info(SignupError)
                raise access_denied_exception


    def auth_oauth(self,provider, params):
        # Advice by Google (to avoid Confused Deputy Problem)
        # if validation.audience != OUR_CLIENT_ID:
        # abort()
        # else:
        # continue with the process
        print params
        access_token = params.get('access_token')
        validation = self._auth_oauth_validate(provider, access_token)

        provider_obj = self.env['auth.oauth.provider'].sud().read(provider)
        provider_type = provider_obj['provider_type']

        if provider_type == 'qq':
            oauth_uid = 'openid'
        elif provider_type == 'weixin':
            oauth_uid = 'openid'
        elif provider_type == 'weibo':
            oauth_uid = 'userid'
        else:
            oauth_uid = 'user_id'

        if not validation.get(oauth_uid):
            raise odoo.exceptions.AccessDenied()
        # retrieve and sign in user
        login = self._auth_oauth_signin(provider, validation, params)
        if not login:
            raise odoo.exceptions.AccessDenied()
        # return user credentials
        return (params['d'], login, access_token)


