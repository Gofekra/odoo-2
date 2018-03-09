odoo.define('theme_app_path', function (require) {
	'use strict';

	var DashboardEchartView = require("ct_dashboard.EchartView");

	DashboardEchartView.include({
		optionBar_Gradient:{
	        from:"#6b7e8c",
	        to:"#022e4f"
    	}
	})
});