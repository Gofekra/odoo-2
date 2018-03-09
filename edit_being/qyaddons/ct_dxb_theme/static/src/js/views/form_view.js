odoo.define('web_enterprise.form_widgets', function (require) {
"use strict";

var config = require('web.config');
var core = require('web.core');
var form_widgets = require('web.form_widgets');

var QWeb = core.qweb;

form_widgets.FieldStatus.include({
    className: "o_statusbar_status",
    render_value: function() {
        this._super.apply(this,arguments)
        this.matchMedia();
    },
    matchMedia:function(){
        var self = this,
            $button = $('<li class="prompt" data-id="draft"><span>当前阶段：</span></li>'),
            result = window.matchMedia("(max-width:767px)");
        if(result.matches){
            self.$el.find("button.prompt").remove();
        }else{
            self.$el.find("button.prompt").remove().end().prepend($button);
        }
    }
});

});