odoo.define('ct.website.editor', function (require) {
'use strict';

var ajax = require('web.ajax');
var core = require('web.core');
var Widget = require('web.Widget');
var base = require('web_editor.base');
var editor = require('web_editor.editor');
var widget = require('web_editor.widget');
var website = require('website.website');

var qweb = core.qweb;
var _t = core._t;

website.TopBar.include({
    delayed_hide: function () {
        _.delay((function () {
            this.do_hide();
            $("[data-toggle='tooltip']").tooltip();
        }).bind(this), 800);
    },
})

})