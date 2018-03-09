odoo.define('web.filter.fidels', function (require) {
	"use strict";
	var core = require('web.core');
	var data_manager = require('web.data_manager');
	var search_inputs = require('web.search_inputs');
	var Widget = require('web.Widget');

	var QWeb = core.qweb;
	var GroupByMenu = require("web.GroupByMenu");

	GroupByMenu.include({
		get_fields: function () {
	        var self = this;
	        if (!this._fields_def) {
	            this._fields_def = data_manager.load_fields(this.searchview.dataset).then(function (fields) {
	                var groupable_types = ['many2one', 'char', 'boolean', 'selection', 'date', 'datetime'];
	                console.table(fields);
	                var filter_group_field = _.filter(fields, function(field, name) {
	                    if (field.store && _.contains(groupable_types, field.type)) {
	                        field.name = name;
	                        return field;
	                    }
	                });
	                self.groupable_fields = _.sortBy(filter_group_field, 'string');

	                self.$menu.append(QWeb.render('GroupByMenuSelector', self));
	                self.$add_group_menu = self.$('.o_add_group');
	                self.$group_selector = self.$('.o_group_selector');
	                self.$('.o_select_group').click(function () {
	                    self.toggle_add_menu(false);
	                    var field = self.$group_selector.find(':selected').data('name');
	                    self.add_groupby_to_menu(field);
	                });
	            });
	        }
	        return this._fields_def;
	    }
	})
})

