odoo.define('change_tree_view', function (require) {
"use strict";

var core = require('web.core');
var Dialog = require('web.Dialog');
var Model = require('web.Model');
var SystrayMenu = require('web.SystrayMenu');
var data = require('web.data');
var Widget = require('web.Widget');
var QWeb = core.qweb;
var Sidebar = require('web.Sidebar');
var pyeval = require('web.pyeval');
var _t = core._t;
   
    function launch_form(self, view) {
        var action = view.getParent().action;;
        var custom_view = new data.DataSet(self, 'change.tree.view.wizard', view.dataset.get_context());
        var domain = new data.CompoundDomain(view.dataset.domain);
    	var rec_name = '';
        pyeval.eval_domains_and_contexts({

            domains: [domain],
            contexts: [custom_view.get_context()]

        }).done(function (result) {

            custom_view.create({
                name: action.name,
                domain: result.domain,
                action_id: action.id,
                view_type: view.fields_view.type,
                view_id:view.id
            }).done(function(custom_view_id) {

            	var fields = $.extend({},view.fields_view.fields);
            	$.each(fields,function(i,v){
            		if(v["__attrs"].invisible){
            			delete fields[i];
					}
				});

                var step1 = custom_view.call('open_action', [[view.fields_view.view_id, action.res_model,fields],custom_view.get_context()]).done(function(result) {
                    var action = result;
                    self.do_action(action);
                    var context={view_id:view.id}
                });

            });

        });
    }


     function recovery_form(self, view) {
        var custom_view = new data.DataSet(self, 'change.tree.view.wizard', view.dataset.get_context());
        pyeval.eval_domains_and_contexts({
        }).done(function() {
			var step1 = custom_view.call('recovery_action', [view.fields_view.view_id]).done(function(result) {
				location.reload();
			});

		});
    }

    /* Extend the Sidebar to add Custom Tree view link in the 'More' menu */
    
	Sidebar.include({
			start: function() {
	            var self = this;
	            this._super(this);
	            self.add_items('other', [
	                    {   label: _t('自定义列表'),
	                        callback: self.on_click_change_tree_view,
	                        classname: 'oe_custom_list' 
	                    },                    
	            ]);
	        },
	        on_click_change_tree_view: function(item) {
	            var view = this.getParent();
	            launch_form.call(this,this,view);
	        },
    });


		Sidebar.include({
			start: function() {
	            var self = this;
	            this._super(this);
	            self.add_items('other', [
	                    {   label: _t('初始化列表'),
	                        callback: self.on_click_recovery_tree_view,
	                        classname: 'recovery_custom_list'
	                    },
	            ]);
	        },
	        on_click_recovery_tree_view: function(item) {
	            var view = this.getParent();
	            recovery_form.call(this,this,view);
	        },
    });

});

