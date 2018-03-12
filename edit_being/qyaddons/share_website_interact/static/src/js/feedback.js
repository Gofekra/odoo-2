odoo.define('cotong.feedback', function (require) {
"use strict";


    
var Class = require('web.Class');
var ajax = require('web.ajax');
var core = require('web.core');
var Widget = require('web.Widget');


    var QWeb = core.qweb;
    var _t = core._t;
    var _lt = core._lt;


// 创建编辑器

Widget.Class.include({

    snippet_templates: function() {
        
        var res = this._super.apply(this, arguments)
         // 使用下载的源码
       var E = ajax.loadJS('/ct_website_interact/static/src/js/wangEditor.min.js')

        var editor = new E($('#editor'))
 
            editor.create();

            return res;
    }

});


})

// $(function(){
        
//         var submit = new Model("ex.submit");s
        
//         var title = $("input.feedback_title").val();
//         var email = $("input.feedback_email").val();
//         var description = $("textarea.o_website_textarea").val();

//         if (title == '' || email == '' || description == '') {
//             alert("不能为空");
//         }

//         if (title && email && description) {

//             submit.call("submit_feedback", [title, email, description]).then(function (data) {
//                 if (data) {
//                     alert("问题提交成功");
//                 } else {
//                     alert("网络连接错误或配置信息没填写完整");
//                 }
//             });
//         }

        
// })
        

