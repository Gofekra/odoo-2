odoo.define('web.theme', function (require) {
'use strict';

var common = require('web.form_common');
var core = require('web.core');
var utils = require('web.utils');
var ajax = require('web.ajax');
var Model = require('web.Model');
var data = require('web.data');
var _t = core._t;
var QWeb = core.qweb;

var FormView = require('web.FormView');
var WebSession = require('web.Session');
var AppSwitcher = require("web_enterprise.AppSwitcher");

var trim = function(val){

    return val.replace(/^\"|\"$/gi,"");
}

var indisable = {
    "ct_web_theme.ct_theme_default":{title:"默认风格",appath:"icon/"},
    "ct_web_theme.ct_theme_blue":{title:"蓝色风格",appath:"theme/blue/icon/"},
    "ct_web_theme.ct_theme_palm":{title:"棕色风格",appath:"theme/palm/icon/"},
    "ct_web_theme.ct_theme_deepblue":{title:"深蓝风格",appath:"theme/deepblue/icon/"}
}

WebSession.include({
    load_modules:function(){

        var model = new Model("res.users"),

            self = this,

            _super = this._super.apply.bind(this._super,this,arguments);    

       return model.call("search_theme").then(function(enable) {

            AppSwitcher.include({
                appath:"/ct_web_theme/static/src/"+indisable[enable].appath
            });

            return ajax.jsonRpc('/theme_switch/theme_customize', 'call', {
                enable: [enable],
                disable: Object.keys(indisable),
                get_bundle: true,
            }).then(function (bundleHTML) {

                var $links = $('link[href*=".assets_backend"]');

                var $newLinks = $(bundleHTML).filter('link');

                var linksLoaded = $.Deferred();

                var nbLoaded = 0;

                $newLinks.on('load', function (e) {

                    if (++nbLoaded >= $newLinks.length) {

                        linksLoaded.resolve();

                    }
                });
                $newLinks.on('error', function (e) {

                    linksLoaded.reject();

                    window.location.hash = "theme=true";

                    window.location.reload();

                });

                $links.last().after($newLinks);

                linksLoaded.then(function () {

                    $links.remove();

                })

                return _super();

            });

        });

       
    }
})

FormView.include({

    to_edit_mode:function(){

        this._super.apply(this,arguments);

        this.update_style("load");

    },
    do_show:function (options) {

        var self = this;

        return this._super.apply(this,arguments).then(function(){

           self.update_style("load");

        });
    },
    save:function(){

        var self = this,

        _super = this._super.apply.bind(this._super,this,arguments);

        return this.update_style("save").then(function(){

            return _super();
        });

    },
	update_style:function(action){

        var self = this,

        selected = this.$el.find("select[name=theme_type]").find("option[value=false]").remove().end();

        if(!(this.datarecord.id == this.session.uid && selected.length)){ return $.Deferred().resolve(); };

        var swithc_select_option = selected.find("option").toArray().map(function(val) {

            return trim(val.value);
        }),

        selected_val = selected.val();

        if(selected_val){

            switch(action){

                case "save":

                return self.load_xml_data([trim(selected_val)],swithc_select_option);

                break;

                case "load":

                return self.reset_xml_data(swithc_select_option,selected);

                break;

                default:

                console.log("加载错误！");

                return $.Deferred().resolve();
                break;

            }

        }

	},
	reset_xml_data:function(enable,option){

        var model = new Model("res.users");

        return model.call("search_theme").then(function(result) {

            option.val('\"'+result+'\"');

        });

	},
	load_xml_data:function(enable,disable){

		var self = this;

		return ajax.jsonRpc('/theme_switch/theme_customize', 'call', {
                enable: enable,
                disable: disable,
                get_bundle: true,
            }).then(function (bundleHTML) {

            	var $links = $('link[href*=".assets_backend"]');

                var $newLinks = $(bundleHTML).filter('link');

                var linksLoaded = $.Deferred();

                var nbLoaded = 0;

                $newLinks.on('load', function (e) {

                    if (++nbLoaded >= $newLinks.length) {

                        linksLoaded.resolve();

                    }
                });

                $newLinks.on('error', function (e) {

                    linksLoaded.reject();

                    window.location.hash = "theme=true";

                    window.location.reload();

                });

                $links.last().after($newLinks);

                return linksLoaded.then(function () {

                    $links.remove();

                    self.$el.removeClass('loading');
                });

            })

	}
})

});