odoo.define('web.ct_feedback', function (require) {
"use strict";

var ajax = require('web.ajax');
var config = require('web.config');
var core = require('web.core');
var Widget = require('web.Widget');
var Model = require('web.Model');
var session = require('web.session');
var Dialog = require('web.Dialog');
var QWeb = core.qweb;
var _t = core._t;
var _lt = core._lt;
var webClient = require('web_enterprise.Menu');

var FeedBack = Widget.extend({
    template:"UserRightMenu",
    willStart: function() {

        if (!window.ace && !this.loadJS_def) {

            this.loadJS_def = ajax.loadJS('/ct_feedback/static/src/js/bootstrap-table.js').then(function () {

                return $.when(ajax.loadJS('/ct_feedback/static/src/js/bootstrap-table-zh-CN.js'),

                    ajax.loadJS('/ct_feedback/static/src/js/wangEditor.min.js')
                );
            });
        }
        return $.when(this._super(), this.loadJS_def);
    },
    init:function(parent,menu_data){
        this._super.apply(this, arguments);
    },
    start: function () {
        var self = this;
        this._super.apply(this, arguments);
        this.$el.parent().find("a.feedback_icon").hover(function (ev) {
            $("img.feedback_img")[0].src = "ct_feedback/static/src/img/feedback2.png"
        }, function (ev) {
            $("img.feedback_img")[0].src = "ct_feedback/static/src/img/feedback1.png"
        });
        this.$el.parent().on('click', 'a[data-menu]', function (ev) {
            ev.preventDefault();
            var f = self['on_menu_' + $(this).data('menu')];
            if (f) {
                f($(this));
            }
        });
    },
    on_menu_feedback: function () {
            var self = this;
            var $help = $(QWeb.render("UserMenu.feedback"));
            var $table = $(QWeb.render("UserData.table"));

            var submit = new Model("ex.submit");
            var question = new Model("question.info");

            //var db = session.db;
            //var feedback_submitter = session.username;
            //var feedback_url = window.location.host;

            $help.find('span.check').click(function (ev) {
                $help.replaceWith($table);
                question.call("search_info").then(function(data){
                    $table.find("#table").bootstrapTable({
                        columns: [{
                                field: 'info_num',
                                title: '问题单号',
                                sortable:true
                        }, {
                                field: 'name',
                                title: '问题标题'
                        }, {
                                field: 'email',
                                title: '电子邮件'
                        }, {
                                field: 'description',
                                title: '问题描述'
                        },{
                                field: 'check_jind',
                                title: '跟踪进度'
                        },{
                                field: 'result_info',
                                title: '处理结果'
                        }],
                        data: data
                    });
                })

                console.log(session)

                // submit.call("get_server_config").then(function (data) {
                //     if (data.error == 1) {
                //         alert("请填写问题反馈的配置信息");
                //     } else {
                //         var login = data.server_username;
                //         var db = data.server_db;
                //         var password = data.server_password;
                //         var url = data.server_url;
                //         var route = url + '/login?db=' + db + '&login=' + login + '&key=' + password;
                //         window.open(route, '_blank');
                //     }
                // });

            });
            // 提交问题按钮 事件
            $help.find('button.feedback_submit').click(function (e) {

                var database = session.db;
                var feedback_submitter = session.name;
                var feedback_url = window.location.host;

                var title = $("input.feedback_title").val();
                var email = $("input.feedback_email").val();
                var description = $("div.feedback_description").html();

                if (title == '' || email == '' || description == '') {
                    alert("不能为空");
                }

                if (title && email && description) {
                    submit.call("submit_feedback", [title, email, description, feedback_url, feedback_submitter, database]).then(function (data) {
                        if (data) {
                            alert("问题提交成功");
                            feedback_dialog.close();
                        } else {
                            alert("网络连接错误或配置信息没填写完整");
                        }
                    });
                }
            });
            // 取消按钮
            $help.find('button.feedback_cancel').click(function (e) {
                feedback_dialog.close();
            });
            // 对话框实例化
            var feedback_dialog = new Dialog(this, {
                title: _t("问题反馈"),
                $content: $help
            });
            feedback_dialog.open();
            this.ContentEditable($help.find('[contenteditable]'));

        },
         ContentEditable:function(Dom){

            var $Editable = $(Dom);

            var editor = new wangEditor($Editable);
            // 表情
            editor.config.emotions = {
                'default': {
                    title: '默认',
                    data: './wangEditor/test/emotions.data'
                }
            };

            editor.config.menus = [
                'source',
                'bold',
                'underline',
                'italic',
                'strikethrough',
                'eraser',
                'forecolor',
                'bgcolor',
                'quote',
                'fontfamily',
                'fontsize',
                'head',
                'unorderlist',
                'orderlist',
                'alignleft',
                'aligncenter',
                'alignright',
                'link',
                'unlink',
                'table',
                'img',
                'video',
                'location',
                'insertcode',
                'undo',
                'redo',
            ];

            editor.create();

    var imgReader = function(item){

    var file = item.getAsFile(),

    reader = new FileReader(),

    dtd  = $.Deferred();

    reader.onload = function(e){

        dtd.resolve(e.target.result)

    };

    reader.readAsDataURL(file);

    return dtd;

    }

    $Editable.on('paste', function(e) {

        var paste,types,items,index,baseData,browser360= null,

             include = ["text/plain", "text/html", "text/rtf", "Files"];

            if(window.clipboardData && clipboardData.setData) {

                 paste = window.clipboardData.items;

            }else{

                paste = (e.originalEvent || e).clipboardData;

            }

            if(!paste){

                return;

            }

            types = paste.types;

            items = paste.items;

            browser360 = paste.getData('text/yne-image-json');

            if(types.length==1 && types[0]==="Files"){

                e.preventDefault();

                if(items[0].kind==='file' && items[0].type.match(/^image/)){


                    imgReader(items[0]).done(function(result){

                        document.execCommand('insertImage', false,result);


                    });

                }

            }else{

                if(types.indexOf('text/html')>-1 && include.indexOf(types[types.length-1])==-1){

                    baseData = browser360?JSON.parse(browser360):JSON.parse(types[types.length-2]);

                    var imgReg = /<img [^>]*data-attr-org-src-id=['"]([^'"]+)[^>]*>/gim,

                    imgsite = /src=['"]([^'"]+)['"]*/gim;

                    if(Object.keys(baseData.data).length){

                        e.preventDefault();

                        document.execCommand('insertHTML',false,paste.getData('text/html').replace(imgReg,function(match,$1){

                        return match.replace(imgsite,'src='+baseData.data[$1].base64);

                        }));

                    }

                }

            }
    });

    }
});


webClient.include({
    start:function(){
         this._super.apply(this, arguments);
         this.check_timezone();
    },
    check_timezone:function(){
        var oe = this.$el.parents().find('.oe_systray');
        this.user_left_menu = new FeedBack(this);
        if(oe.length){
            this.user_left_menu.appendTo(oe);
        }else{
            oe = this.$el.parents().find('.o_menu_systray>.o_no_notification').last().get(0);
            this.user_left_menu.insertAfter(oe)
        }
        
    }
})

return FeedBack;

});
