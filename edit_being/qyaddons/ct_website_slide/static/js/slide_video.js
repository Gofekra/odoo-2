/**
 * Created by SHQT on 2017/7/6.
 */
odoo.define('ct_slide_video', function (require) {

    var ajax = require('web.ajax');
    var core = require('web.core');
    var form_common = require('web.form_common');
    var SystrayMenu = require('web.SystrayMenu');
    var Widget = require('web.Widget');
    var Model = require('web.Model');
    var session = require('web.session');
    var Dialog = require('web.Dialog');
    var QWeb = core.qweb;

    var slide_video = form_common.AbstractField.extend({
         init:function(){
             this._super.apply(this,arguments);

         },
         start:function(){
                  var self = this;
                  var signin = new Model("slide.slide");
                   signin.call("search_url",[this.view.datarecord.id]).then(function(result){
                    if(result){
                        self.$el.html(QWeb.render("slide_video", {
                            video:result
                        }))
                    }
                })
         }
    });
    core.form_widget_registry.add('slide_video', slide_video);
});