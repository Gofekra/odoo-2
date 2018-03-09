odoo.define('inherit.show.Message.CrashManager', function (require) {
"use strict";

var ajax = require('web.ajax');
var core = require('web.core');
var Dialog = require('web.Dialog');

var QWeb = core.qweb;
var _t = core._t;
var _lt = core._lt;
var CrashManager = require("web.CrashManager");

CrashManager.include({
	show_error: function(error) {
        if (!this.active) {
            return;
        }
        // || error.exception_type=='internal_error'  error.type=='客户端错误'
        if(error.code ==100  || (error.data.exception_type=='internal_error' &&  error.data.message.indexOf('404: Not Found')>=0)) {
            error = $.extend(error,{
                message:"企通云提示您：",
                data:{
                    debug:"当前页面已失效,请刷新页面后重试!"
                }
            });
        }


        new Dialog(this, {
            title: "企通云 " + _.str.capitalize(error.type),
            $content: QWeb.render('CrashManager.error', {error: error})
        }).open();

    }
})
})