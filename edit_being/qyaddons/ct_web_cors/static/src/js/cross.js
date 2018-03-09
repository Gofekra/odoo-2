if(window.parent.length){
	window.parent.postMessage(odoo.csrf_token,'http://portal.qitongyun.cn');
	window.parent.postMessage(odoo.csrf_token,'http://wx.qitongyun.cn');
}