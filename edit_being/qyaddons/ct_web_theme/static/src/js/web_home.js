odoo.define('web_home_theme', function (require) {
"use strict";

var ajax = require('web.ajax');
var config = require('web.config');
var core = require('web.core');
var Widget = require('web.Widget');
var Model = require('web.DataModel');
var session = require('web.session');
var ActionManager = require('web.ActionManager');
var _t = core._t;
var _lt = core._lt;
var QWeb = core.qweb;

function visit(tree, callback, path) {
    path = path || [];
    callback(tree, path);
    _.each(tree.children, function(node) {
        visit(node, callback, path.concat(tree));
    });
}

function is_mobile() {
    return config.device.size_class <= config.device.SIZES.XS;
}


var WebHome = Widget.extend({
    init:function(parent,menu_data){
        var self = this;
        this._super.apply(this, arguments);
        if(Object.prototype.toString.call(menu_data.children) == '[object Array]'){
            this.menu_data = this.process_menu_data(menu_data);
            this.state = this.get_initial_state();

        }else{
            this.client().then(function(menu_data){
                self.menu_data = self.process_menu_data(menu_data);
                self.state = self.get_initial_state();
                self.$el.html(QWeb.render('AppSwitcher.WebHome', { widget: self }));
                self.start();
            });
        }
    },
    start: function () {
        this._super.apply(this, arguments);
        //显示仪表盘控件
        this.render();
    },
    client:function(){
        return this.load_menus().then(function(menu_data) {
            return menu_data;
        });
    },
    load_menus: function () {
        var Menus = new Model('ir.ui.menu');
        return Menus.call('load_menus', [core.debug], {context: session.user_context}).then(function(menu_data) {
            for (var i = 0; i < menu_data.children.length; i++) {
                var child = menu_data.children[i];
                if (child.action === false) {
                    while (child.children && child.children.length) {
                        child = child.children[0];
                        if (child.action) {
                            menu_data.children[i].action = child.action;
                            break;
                        }
                    }
                }
            }
            return menu_data;
        });
    },
    get_initial_state: function () {
        return {
            apps: _.where(this.menu_data, {is_app: true}),
            menu_items: [],
            focus: null,  // index of focused element
            is_searching: is_mobile(),
        };
    },
    process_menu_data: function(menu_data) {
        var result = [];
        visit(menu_data, function (menu_item, parents) {
            if (!menu_item.id || !menu_item.action) {
                return;
            }
            var item = {
                label: _.pluck(parents.slice(1), 'name').concat(menu_item.name).join(' / '),
                id: menu_item.id,
                xmlid: menu_item.xmlid,
                action: menu_item.action ? menu_item.action.split(',')[1] : '',
                is_app: !menu_item.parent_id,
                web_icon: menu_item.web_icon,
            };

            if (!menu_item.parent_id) {
                if (menu_item.web_icon_data) {
                    item.web_icon_data = 'data:image/png;base64,' + menu_item.web_icon_data;
                } else if (item.web_icon) {
                    var icon_data = item.web_icon.split(',');
                    var $icon = $('<div>')
                        .addClass('o_app_icon')
                        .css('background-color', icon_data[2])
                        .append(
                            $('<i>')
                                .addClass(icon_data[0])
                                .css('color', icon_data[1])
                        );
                    item.web_icon = $icon[0].outerHTML;
                } else {
                    item.web_icon_data = '/ct_web_theme/static/src/img/default_icon_app.png';
                }
            } else {
                item.menu_id = parents[1].id;
            }
            result.push(item);
        });
        return result;
    },
    calendar:function(){

        var Model = require('web.Model');

        var dashboard_model = new Model('ct.dashboard');

        dashboard_model.call('get_config').then(function (result) {

                if (result.show) {

                    for (var i = 0; i < result.show.length; i++) {

                        $("#" + result.show[i]).show();
                    }
                }

                if (result.hide) {

                    for (var i = 0; i < result.hide.length; i++) {

                        $("#" + result.hide[i]).hide();
                    }
                }
        });
        var calendar = this.$el.find("#calendar");
        var self = this;
        if(calendar.length && this.session.module_loaded["calendar"]){
            setTimeout(function(){
                var am = new ActionManager(self);
                am.appendTo(calendar).then(function () {
                    am.do_action({
                    "groups_id":[],
                    "domain":[],
                    "xml_id":"calendar.action_calendar_event",
                    "res_model":"calendar.event",
                    "search_view_id":[false,"calendar.event.search"],
                    "views":[[false,"calendar"]],
                    "src_model":false,
                    "usage":false,
                    "flags":{
                        "search_view":true,
                        "sidebar":false,
                        "views_switcher":false,
                        "action_buttons":false,
                        "pager":false,
                        "headless":true,
                        "low_profile":true,
                        "display_title":false,
                        "search_disable_custom_filters":true,
                        "list":{"selectable":false}
                    },
                    "res_id":0,
                    "view_id":[false,"calendar.event.calendar"],
                    "view_mode":"calendar,list,form",
                    "multi":false,
                    "target":"current",
                    "auto_search":true,
                    "type":"ir.actions.act_window",
                    "filter":false,
                    "context":self.session.user_context}).then(function(){
                        if (am.inner_widget) {
                    var new_form_action = function(id, editable) {
                        var new_views = [];
                        _.each(action_orig.views, function(view) {
                            new_views[view[1] === 'form' ? 'unshift' : 'push'](view);
                        });
                        if (!new_views.length || new_views[0][1] !== 'form') {
                            new_views.unshift([false, 'form']);
                        }
                        action_orig.views = new_views;
                        action_orig.res_id = id;
                        action_orig.flags = {
                            form: {
                                "initial_mode": editable ? "edit" : "view",
                            }
                        };
                        self.do_action(action_orig);
                    };
                    var list = am.inner_widget.views.list;
                    if (list) {
                        list.loaded.done(function() {
                            $(list.controller.groups).off('row_link').on('row_link', function(e, id) {
                                new_form_action(id);
                            });
                        });
                    }
                    var kanban = am.inner_widget.views.kanban;
                    if (kanban) {
                        kanban.loaded.done(function() {
                            kanban.controller.open_record = function(event, editable) {
                                new_form_action(event.data.id, editable);
                            };
                        });
                    }
                    }
                    });  
                    
                    am.do_action = self.do_action.bind(self);
                    am.current_action_updated = function() {};
            })
            },0)
        }
    },
    fullCalendar:function(){

    },
    selected_item: function (event,modelName) {
        this.do_action({
            type: 'ir.actions.act_window',
            res_model: modelName,
            res_id: $(event.currentTarget).data('id'),
            views: [[false, 'form']],
            target: 'current',
            context: {},
        });
    },
    DataMessage:function(element){

        var date = new Date(),

        d = {

            Y:date.getFullYear(),

            M:date.getMonth()+1,

            D:date.getDate(),

            h:date.getHours(),

            i:date.getMinutes(),

            s:date.getSeconds(),

            ms:date.getMilliseconds(),

            weekDay:date.getDay(),

            __proto__:{

                week:function(){

                    var start = new Date(this.Y,this.M-1,this.D,0,0,0);

                    var now = new Date(this.Y,0,1,0,0,0);

                    var Time = (start-now)/(24*60*60*1000);

                    var WeekDay = (this.weekDay || 7);

                    return Math.ceil((Math.ceil(Time)+WeekDay)/7);

                }
            }

        }

        this.$(element).html(d.Y+' 年 '+d.M+' 月 <b>'+d.D+'</b> 日 '+d.week()+' 周 ')
    },
    AjaxLis:function(element,url,obj){

        //新增代码

        var getMode = function(Model){

            _self.$(element).find('li').on('click',function(event){

                _self.selected_item(event,Model);

            })

            return true;

        }

        var Margin = function(Time){

            var s = 1000,
                i = s*60,
                h = i*60,
                D = h*24,
                M = D*30,
                Y = M*12,
                district = h*8,
                Time = new Date() - (new Date(Time).getTime()+district),
                val = null;

                if((val = Math.floor(Time/Y))>1){

                    val =  val+"年前";

                }else if((val = Math.floor(Time/M))>=1){

                    val = val+"月前";

                }else if((val = Math.floor(Time/D))>=1){

                    val = val+"天前";

                }else if((val = Math.floor(Time/h))>=1){

                    val = val+"小时前";

                }else if((val = Math.floor(Time/i))>=1){

                    val = val+"分钟前";

                }else{

                    val = "现在";

                }

                return val;

        }

        var _self = this;

        var cutTable = {

            backlist:function(s,callback){

                _self.getAjax(url,function(data){

                    if(!data.length){

                        return false;

                    }

                    if(callback){

                        callback(data);

                    }

                    var mnsj;

                    mnsj = !!s?_self.JsonSort(data,s):data;

                    mnsj = data.map(function(val,name){

                      return '<li data-id="'+data[name].id+'"><div class="o_thread_message_core"><p class="o_mail_info"><strong>'+val[s[0]]+'</strong> - <small class="o_mail_timestamp" title="'+new Date(val[s[2]])+'">'+Margin(val[s[2]])+'</small></p><p class="o_mail_info"><strong>'+val[s[1]]+'</strong> - <small class="o_mail_timestamp">'+val[s[4]]+'</small></p><p>'+val[s[3]]+'</p></div></li>';

                    }).join('');

                   $(_self.$el.find(element).get(0)).html(mnsj);

                   data[0]['model_name'] && getMode(data[0]['model_name']);

                });

            },
            worklist:function(s,callback){

                _self.getAjax(url,function(data){

                    var mnsj;

                    if(!data.name.length){

                        return false;

                    }

                    if(callback){

                        callback(data);

                    }

                    var el = _self.$el.find(element),
                        navtabs = el.find("ul.nav-tabs"),
                        navtabs_li = navtabs.find("li"),
                        tabpane = el.find(".tab-pane");
                    data.name.filter(function(val){
                        navtabs.append($(navtabs_li.clone(true)).find("a").html(val).end());
                        var tab = $(tabpane.clone(true)),
                            list = tab.find(".todo-list"),
                            li = list.find("li");
                        data["json"][val].filter(function(json){
                            list.append($(li.clone(true)).data("id",json.id).find("a").html(json["主题"]).end().bind("click",function(event){
                                _self.selected_item(event,json.model_name);
                                event.preventDefault();
                                return false;
                            }));
                        });
                            el.append(tab);
                            li.empty().remove();
                    });
                    navtabs_li.empty().remove();
                    tabpane.empty().remove();
                    navtabs.find("li").first().addClass("active");
                    el.find(".tab-pane").first().addClass("active");

                });

            }
        }

        try{

            return cutTable[obj.cut](obj.Sort);

        }catch(e){

            console.log(e)

        }
    },
    JsonSort:function(d,s){

        var sortData={};

            sortData = d.map(function(value){

                var data={};

                s.forEach(function(val,index){

                    data[val] = value[val];

                });

                return data;

            });

            return sortData;
    },
    getAjax:function(url,callback){

         ajax.jsonRpc(url, 'call', {}).done(function(result){

            if(callback){

                callback(result);
            }

    });
    },
    render: function() {
        //新增代码
        this.DataMessage('.dataInfo');
        this.$el.find("#routine .nav-tabs li").mouseover(function(e) {
            e.preventDefault();
            var index = $(this).index();
            $(this).addClass('active').siblings().removeClass('active');
            $("#routine .fade").eq(index).addClass('active').siblings("#routine .fade").removeClass('active');
        });
        this.AjaxLis('#todolist','/mail/redirect_to_messaging',{cut:'backlist',Sort:['用户','主题','日期','备注','阶段']});
        // this.AjaxLis('#routine','/note/redirect_to_note',{cut:'worklist'});
        this.fullCalendar();
        this.calendar();
    }

});
core.action_registry.add('WebHome', WebHome);

return WebHome;
});
