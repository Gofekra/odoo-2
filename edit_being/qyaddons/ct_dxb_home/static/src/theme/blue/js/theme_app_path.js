odoo.define('theme_app_path', function (require) {
	'use strict';

	var DashboardEchartView = require("ct_dashboard.EchartView");

	DashboardEchartView.include({
		optionBar_Gradient:{
	        from:"#0083c7",
	        to:"#02344e"
    	}
	})
});