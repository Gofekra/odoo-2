odoo.define('web_printscreen_zb', function (require) {
"use strict";

var core = require('web.core');
var ListView = require('web.ListView');
var Model = require('web.DataModel');
var session = require('web.session');
var Widget = require('web.Widget');
var formats = require('web.formats');
var ajax = require('web.ajax');
var QWeb = core.qweb;
var _t = core._t;
var _lt = core._lt;

ListView.include({
	export_to_excel: function(export_type) {
            var self = this;
            var export_type = export_type;
            var view = this.getParent();
            // Find Header Element
            var header_eles = self.$el.find('.o_list_view');
            var header_name_list = [];
            $.each(header_eles,function(){;
                var $header_ele = $(this);
                var header_td_elements = $header_ele.find('th');
                $.each(header_td_elements,function(){
                    var $header_td = $(this);
                    var text = $header_td.text().trim() || "";
                    var data_id = $header_td.attr('data-id');
                    if (text && !data_id){
                        var data_id = 'group_name';
                    }
                    header_name_list.push({'header_name': text.trim(), 'header_data_id': data_id});
                   // }
                });
            });

            //Find Data Element
            var data_eles = self.$el.find('.o_list_view > tbody > tr');
            var export_data = [];
            $.each(data_eles,function(){
                var data = []
                var $data_ele = $(this)
                var is_analysis = false
                if ($data_ele.text().trim()){
                //Find group name
	                var group_th_eles = $data_ele.find('th');
	                $.each(group_th_eles,function(){
	                    var $group_th_ele = $(this);
	                    var text = $group_th_ele.text().trim() || "";
	                    var is_analysis = true;
	                    data.push({'data': text, 'bold': true})
	                });
                    if($data_ele.find('td:eq(0) :checkbox:checked').length){
	                var data_td_eles = $data_ele.find('td')
	                $.each(data_td_eles,function(){
	                    var $data_td_ele = $(this)
	                    var text = $data_td_ele.text().trim() || ""
	                    if ($data_td_ele && $data_td_ele[0].classList.contains('o_list_number') && !$data_td_ele[0].classList.contains('oe_list_field_float_time')){
	                        var text = text.replace('%', '')
//	                        text = instance.web.parse_value(text, { type:"float" })
	                        //#787
	                        var text = formats.parse_value(text, { type:"string" });
	                        data.push({'data': text || "", 'number': true})
	                    }
	                    else{
	                        data.push({'data': text})
	                    }
	                });
	                export_data.push(data)
                }
                }
            });

            //Find Footer Element

            var footer_eles = self.$el.find('.o_list_view > tfoot> tr');
            $.each(footer_eles,function(){
                var data = []
                var $footer_ele = $(this)
                var footer_td_eles = $footer_ele.find('td')
                $.each(footer_td_eles,function(){
                    var $footer_td_ele = $(this)
                    var text = $footer_td_ele.text().trim() || ""
                    if ($footer_td_ele && $footer_td_ele[0].classList.contains('o_list_number')){
                        //var text = instance.web.parse_value(text, { type:"float" })
			var text = formats.parse_value(text, { type:"float" });
                        data.push({'data': text || "", 'bold': true, 'number': true})
                    }
                    else{
                        data.push({'data': text, 'bold': true})
                    }
                });
                export_data.push(data)
            });

            //Export to excel
            $.blockUI();
            var url;
            if(export_type === 'excel'){
                url = '/web/export/zb_excel_export'
            }else{
                console.log(export_data);
                console.log(header_name_list);
                url = '/web/export/zb_pdf_export'

            }
             new Model("res.users").get_func("read")(this.session.uid, ["company_id"]).then(function(res) {
                    new Model("res.company").get_func("read")(res[0]['company_id'][0], ["name"]).then(function(result) {
                        view.session.get_file({
                             url: url,
                             data: {data: JSON.stringify({
                                    uid: view.session.uid,
                                    model : self.model,
                                    headers : header_name_list,
                                    rows : export_data,
                                    company_name: result['name']
                             })},
                             complete: $.unblockUI
                         });
                    });
                });
        },
    render_buttons: function() {
        var self = this;

        this._super.apply(this, arguments); // Sets this.$buttons

        this.$buttons.find("a#button_export_excel").click(function(event){
        		self.export_to_excel("excel");
                return false;
    	});

    	this.$buttons.find("a#button_export_pdf").click(function(event){
        		self.export_to_excel("pdf");
                return false;
    	});
        
    }
});

});
