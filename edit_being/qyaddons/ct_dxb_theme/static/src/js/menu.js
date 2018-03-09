odoo.define('Pos.web.Menu', function (require) {
"use strict";
var core = require('web.core');
var session = require('web.session');
var Widget = require('web.Widget');
var Model = require('web.Model');

var QWeb = core.qweb;

var web_Menu = require("web.Menu");

web_Menu.include({
	open_menu:function(id){
		this.current_menu = id;
        session.active_id = id;
        var $clicked_menu, $sub_menu, $main_menu;
        $clicked_menu = this.$el.add(this.$secondary_menus).find('a[data-menu=' + id + ']');
        this.trigger('open_menu', id, $clicked_menu);

        if (this.$secondary_menus.has($clicked_menu).length) {
            $sub_menu = $clicked_menu.parents('.oe_secondary_menu');
            $main_menu = this.$el.find('a[data-menu=' + $sub_menu.data('menu-parent') + ']');
        } else {
            $sub_menu = this.$secondary_menus.find('.oe_secondary_menu[data-menu-parent=' + $clicked_menu.attr('data-menu') + ']');
            $main_menu = $clicked_menu;
        }
        
        // Activate current main menu
        this.$el.find('.active').removeClass('active');
        $main_menu.parent().addClass('active');

        // Show current sub menu
        this.$secondary_menus.find('.oe_secondary_menu').hide();
        $sub_menu.show();

        // Hide/Show the leftbar menu depending of the presence of sub-items
        this.$secondary_menus.toggleClass('o_hidden', !$sub_menu.children().length);

        // Activate current menu item and show parents
         $clicked_menu.parent().addClass('active').siblings(".oe_secondary_menu_section").removeClass('active');
        // this.$secondary_menus.find('.active').removeClass('active');
        if ($main_menu !== $clicked_menu) {
            $clicked_menu.parents().removeClass('o_hidden');
            if ($clicked_menu.is('.oe_menu_toggler')) {
                $clicked_menu.toggleClass('oe_menu_opened').siblings('.oe_secondary_submenu:first').toggleClass('o_hidden');
            } else {
                $clicked_menu.parent().addClass('active');
            }
        }
        // add a tooltip to cropped menu items
        this.$secondary_menus.find('.oe_secondary_submenu li a span').each(function() {
            $(this).tooltip(this.scrollWidth > this.clientWidth ? {title: $(this).text().trim(), placement: 'right'} :'destroy');
        });

        var _that = this;

        this.$el.parent().find("#dateRange").remove();

		new Model('ir.http').call('get_client').then(function(result){

			var parent_id = $sub_menu.data('menu-parent');

			_that.$el.addClass('show').html($(QWeb.render("pos_navbar",{
				menu_data:result.children.filter(function(menu){
					return menu.id == parent_id
				}),
				active_id:id,
				debug:odoo.debug
			})))

		})
	}
})
})