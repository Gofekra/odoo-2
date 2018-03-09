odoo.define('theme_app_path', function (require) {
	'use strict';

	var AppSwitcher = require("web_enterprise.AppSwitcher"),

		path = 'blue';

	AppSwitcher.include({
		appath:"/ct_web_theme/static/MenuImage/switch/"+path+"/"
	});


	var DashboardEchartView = require("ct_dashboard.EchartView");

	DashboardEchartView.include({
		optionBar_Gradient:{
	        from:"#0083c7",
	        to:"#02344e"
    	}
	})
});