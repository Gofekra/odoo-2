/**
 * Created by SHQT on 2017/7/6.
 */
odoo.define('ct_voice_marketing', function (require) {

    var ajax = require('web.ajax');
    var core = require('web.core');
    var form_common = require('web.form_common');
    var SystrayMenu = require('web.SystrayMenu');
    var Widget = require('web.Widget');
    var Model = require('web.Model');
    var session = require('web.session');
    var Dialog = require('web.Dialog');
    var QWeb = core.qweb;

    var voice_audio = form_common.AbstractField.extend({
         template:"slide_audio",
         init:function(){

            this._super.apply(this,arguments);

         },
         start:function(){

            var self = this,

                signin = new Model("template.voice");

            self.$("#voice_audio").hover(function(){

                var that = this;

                signin.call("search_url",[self.view.datarecord.id]).then(function(result){

                    if(result){

                        self.create_audio(result,"播放语音中...");
                        
                    }

                })
            },function(){

                 self.trigger_audio_Up("移入播放语音");
            })

         },
         create_audio:function(url,text){

            this.$("#voice_audio .sound-trigger").trigger("mouseup").off().find(".sound-trigger__speach").text(text).end().easyAudioEffects({
                 mp3 : url,
                 eventType : "click",
                 playType : "gate"
            });

            this.$("#voice_audio .sound-trigger").trigger("mousedown");

         },
         trigger_audio_Up:function(text){

            this.$("#voice_audio .sound-trigger").find(".sound-trigger__speach").text(text).end().trigger('mouseup').off();
         }
    });

    core.form_widget_registry.add('voice_audio', voice_audio);
});