odoo.define('ct_web_home.AppSwitcher', function (require) {
"use strict";

var ajax = require('web.ajax');
var config = require('web.config');
var core = require('web.core');
var Widget = require('web.Widget');
var utils = require('web.utils');
var _t = core._t;


var MailChatWindow = require('mail.ChatWindow');
var WebControlPanel = require('web.ControlPanel');
var WebEditor = require('web_editor.backend');
var WebProgressBar = require('web.ProgressBar');
var WebFormRelational = require('web.form_relational');


WebControlPanel.include({
    _update_search_view:function(){
        this._super.apply(this,arguments);
        if($(".o_cp_searchview:hidden").length && $(".o_cp_left div:empty").length==2){
            $(".o_control_panel").addClass("o_control_panel_modify");
        }else{
            $(".o_control_panel.o_control_panel_modify").removeClass("o_control_panel_modify");
        }
    }
})

var HEIGHT_OPEN = '400px';
var HEIGHT_FOLDED = '62px';

MailChatWindow.include({
    start:function(){
        this._super();
        if (this.folded) {
            this.$el.css('height', HEIGHT_FOLDED);
        }
    },
    fold: function () {
        this.$el.animate({
            height: this.folded ? HEIGHT_FOLDED : HEIGHT_OPEN
        });
    }
})

WebEditor.FieldTextHtmlSimple.include({
    reset_history: function () {
        var history = this.$content.data('NoteHistory');
        if (history) {
            history.reset();
            this.$('.note-toolbar').find('button[data-event="undo"]').attr('disabled', true);
        }
    }
})

WebProgressBar.include({
        unitConversion:function(number){

        var unit ='',

            data = number;

        switch(Math.floor(number.toString().length - 3)){

                case 1:

                data = Math.floor(data/1000);

                unit = '千';

                    break;

                case 2:
                case 3:
                case 4:
                case 5:

                data = Math.floor(data/(10000));

                unit = '万';

                    break;

                case 6:
                case 7:

                data = Math.floor(data/(100000000));

                unit = '亿'

                    break;

                default:

                    break;

            }

            return data+unit;

    },
    _render_value: function(v) {
        var value = this.value;
        var max_value = this.max_value;
        if(!isNaN(v)) {
            if(this.edit_max_value) {
                max_value = v;
            } else {
                value = v;
            }
        }
        value = value || 0;
        max_value = max_value || 0;

        var widthComplete;
        if(value <= max_value) {
            widthComplete = value/max_value * 100;
        } else {
            widthComplete = 100;
        }

        this.$('.o_progress').toggleClass('o_progress_overflow', value > max_value);
        this.$('.o_progressbar_complete').css('width', widthComplete + '%');

        if(this.readonly) {
            if(max_value !== 100) {
                this.$('.o_progressbar_value').html(this.unitConversion(value) + " / " + this.unitConversion(max_value));
            } else {
                this.$('.o_progressbar_value').html(utils.human_number(value) + "%");
            }
        } else if(isNaN(v)) {
            this.$('.o_progressbar_value').val(this.edit_max_value ? max_value : value);
        }
    }
});

// WebFormRelational.FieldMany2One.include({
//     render_editable:function(){
//         this._super.apply(this,arguments);
//         $(".ui-autocomplete,.bootstrap-datetimepicker-widget").hover($.noop(),function(){
//             $(".o_form_input,.o_datepicker_input").blur();
//             $(this).hide();
//         });
//     }
// })

// var MailChatThread = require('mail.ChatThread');
// function time_from_now(date) {
//
//     var date = new Date(date);
//
//     return "时间："+date.getFullYear()+"-"+(date.getMonth()+1)+"-"+date.getDate()+" "+date.getHours()+":"+date.getMinutes()+":"+date.getSeconds();
//
// }
//
// MailChatThread.include({
//     _preprocess_message:function(message){
//         var msg = _.extend({}, message);
//
//         msg.date = moment.min(msg.date, moment());
//         msg.hour = time_from_now(msg.date);
//
//         var date = msg.date.format('YYYY-MM-DD');
//         if (date === moment().format('YYYY-MM-DD')) {
//             msg.day = _t("Today");
//         } else if (date === moment().subtract(1, 'days').format('YYYY-MM-DD')) {
//             msg.day = _t("Yesterday");
//         } else {
//             msg.day = msg.date.format('LL');
//         }
//
//         if (_.contains(this.expanded_msg_ids, message.id)) {
//             msg.expanded = true;
//         }
//
//         msg.display_subject = message.subject && message.message_type !== 'notification' && !(message.model && (message.model !== 'mail.channel'));
//         msg.is_selected = msg.id === this.selected_id;
//         return msg;
//     }
// });

});
