odoo.define('theme_app_path', function (require) {
	'use strict';

	var DashboardEchartView = require("ct_dashboard.EchartView");

	DashboardEchartView.include({
		optionBar_Gradient:{
	        from:"#a40000",
	        to:"#380000"
    	}
	})
	
});