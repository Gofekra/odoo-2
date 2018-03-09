odoo.define('inher_website.im_livechat', function (require) {
"use strict";
var bus = require('bus.bus').bus;
var config = require('web.config');
var core = require('web.core');
var session = require('web.session');
var time = require('web.time');
var utils = require('web.utils');
var Widget = require('web.Widget');

var ChatWindow = require('mail.ChatWindow');

var _t = core._t;
var QWeb = core.qweb;
var im_livechat = require("im_livechat.im_livechat");

im_livechat.LivechatButton.include({
    load_qweb_template:function(){
        return $.when(
            $.get('/mail/static/src/xml/chat_window.xml'),
            $.get('/mail/static/src/xml/thread.xml'),
            $.get('/ct_im_livechat/static/xml/im_livechat.xml')
        ).then(function (chat_window, mail_thread, livechat) {
            // results are triplets of [dom: XMLDocument, status: String, xhr: jqXHR]
            QWeb.add_template(chat_window[0]);
            QWeb.add_template(mail_thread[0]);
            QWeb.add_template(livechat[0]);
        });
    }
})

});
