# -*- coding: utf-8 -*-
from  odoo import http
#----------------------------------------------------------
import logging
try:
    import psutil
except ImportError:
    psutil = None
import odoo
from odoo.tools import ustr, consteq, frozendict
_logger = logging.getLogger(__name__)



class error_message(http.JsonRequest):

    def __init__(self):

        self._handle_exception()


    def _handle_exception(self, exception):

        print "###################"
        """Called within an except block to allow converting exceptions
           to arbitrary responses. Anything returned (except None) will
           be used as response."""
        try:
            return super(error_message, self)._handle_exception(exception)
        except Exception:
            if not isinstance(exception, (odoo.exceptions.Warning, http.SessionExpiredException, odoo.exceptions.except_orm)):
                _logger.exception("Exception during JSON request handling.")
            print serialize_exception(exception)
            error = {

                    'code': 200,
                    'message': "Clound prompts you：", #
                    'data': serialize_exception(exception)
            }
            if isinstance(exception, http.AuthenticationError):
                error['code'] = 100
                error['message'] = "Clound prompts you：" #
            if isinstance(exception, http.SessionExpiredException):
                error['code'] = 100
                error['message'] = "Clound prompts you:"#
            # sys.stdout.write('Hello World')
            return self._json_response(error=error)

def serialize_exception(e):

    tmp = {
        "name": type(e).__module__ + "." + type(e).__name__ if type(e).__module__ else type(e).__name__,
        # "debug": traceback.format_exc(),
        "debug":'The current page has expired. Please try again after refreshing!',# '当前网页已失效，请刷新后重试！',
        "message": ustr(e),
        "arguments": http.to_jsonable(e.args),
        "exception_type": "internal_error"
    }
    if isinstance(e, odoo.exceptions.UserError):
        tmp["exception_type"] = "user_error"
    elif isinstance(e, odoo.exceptions.Warning):
        tmp["exception_type"] = "warning"
    elif isinstance(e, odoo.exceptions.RedirectWarning):
        tmp["exception_type"] = "warning"
    elif isinstance(e, odoo.exceptions.AccessError):
        tmp["exception_type"] = "access_error"
    elif isinstance(e, odoo.exceptions.MissingError):
        tmp["exception_type"] = "missing_error"
    elif isinstance(e, odoo.exceptions.AccessDenied):
        tmp["exception_type"] = "access_denied"
    elif isinstance(e, odoo.exceptions.ValidationError):
        tmp["exception_type"] = "validation_error"
    elif isinstance(e, odoo.exceptions.except_orm):
        tmp["exception_type"] = "except_orm"
    return tmp
