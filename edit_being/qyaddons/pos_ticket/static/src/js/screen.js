// odoo.define('pos_theme.screens', function (require) {
// "use strict";
// 	var core = require('web.core');
// 	var QWeb = core.qweb;
// 	var _t = core._t;
// 	var screens = require('point_of_sale.screens');
// 	screens.ReceiptScreenWidget.include({
// 		print_web:function(){
// 			window.print();
//         	this.pos.get_order()._printed = true;
// 		},
// 		print_xml:function(){
//             var env = {
//                 widget:  this,
//                 order: this.pos.get_order(),
//                 receipt: this.pos.get_order().export_for_printing(),
//                 paymentlines: this.pos.get_order().get_paymentlines()
//             };
//             var receipt = QWeb.render('XmlFreeTicket',env);
//
//             this.pos.proxy.print_receipt(receipt);
//             this.pos.get_order()._printed = true;
// 		}
//
// 	})
// })