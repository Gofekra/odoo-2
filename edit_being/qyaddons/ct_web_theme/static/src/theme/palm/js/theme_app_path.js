odoo.define('theme_app_path', function (require) {
	'use strict';

	var DashboardEchartView = require("ct_dashboard.EchartView");

	DashboardEchartView.include({
		optionBar_Gradient:{
	        from:"#8b7f69",
	        to:"#4e3902"
    	}
	})
});