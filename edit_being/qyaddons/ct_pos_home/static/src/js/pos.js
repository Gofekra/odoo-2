odoo.define('point_of_sale.Match', function (require) {
"use strict";

	function IsPC() {
	    var userAgentInfo = navigator.userAgent;
	    var Agents = ["Android", "iPhone",
	                "SymbianOS", "Windows Phone",
	                "iPad", "iPod"];
	    var flag = true;
	    for (var v = 0; v < Agents.length; v++) {
	        if (userAgentInfo.indexOf(Agents[v]) > 0) {
	            flag = false;
	            break;
	        }
	    }
	    return flag;
	}

    if (!IsPC()){
        var Match = window.matchMedia("(orientation:portrait)");
        if(Match.matches){
        	alert("为了您更好的操作，请在横屏设置下操作系统！谢谢。");
        }
    	
    }
})
