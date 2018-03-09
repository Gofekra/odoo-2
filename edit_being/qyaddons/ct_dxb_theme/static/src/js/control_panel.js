odoo.define('pos.web.ControlPanel', function (require) {
"use strict";
var web_ControlPanel = require("web.ControlPanel");
web_ControlPanel.include({
	_update_search_view:function(){
		this._super.apply(this, arguments);
		$("#oe_main_menu_navbar .collapse").append(this.nodes.$searchview.addClass("nav navbar-nav navbar-right oe_user_menu_placeholder"));
	}
})

})