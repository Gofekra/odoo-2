odoo.define('cotong.website.style.navbar', function (require) {
"use strict";

var Class = require('web.Class');
var ajax = require('web.ajax');
var core = require('web.core');
var Widget = require('web.Widget');
var editor = require('web_editor.editor');
var animation = require('web_editor.snippets.animation');
var options = require('web_editor.snippets.options');

var qweb = core.qweb;
var _t = core._t;

ajax.loadXML('/web_editor/static/src/xml/snippets.xml', qweb);

var snippets = require('web_editor.snippet.editor');


snippets.Class.include({
	compute_snippet_templates:function(){

		var res = this._super.apply(this, arguments);

		var li;

		var blockMenu = $("<div class='o_panel blockMenu'><div class='o_panel_header'><ul class='list-unstyled'></ul></div></div>");

		this.$el.find("#o_scroll").prepend(blockMenu);

		this.$el.find("#o_scroll .o_panel[id]").each(function(index,self){

			li = $("<li></li>").append($(this).find(".o_panel_header").html()).on("click",function(){

				$(self).find(".o_panel_body").slideToggle("slow").parent().siblings(".o_panel[id]").find(".o_panel_body").slideUp("slow");
			
				$(this).addClass('active').siblings().removeClass('active');
			})

			blockMenu.find(".o_panel_header ul").append(li);

			$(self).find(".o_panel_header").hide();

		}).first().find(".o_panel_body").show();

		blockMenu.find(".o_panel_header ul li:first-of-type").addClass('active');



		// this.$el.find("#o_scroll .o_panel .o_panel_header").on("click",function(){

		// 	$(this).next(".o_panel_body").slideToggle("slow");
		// })

		return res;
	}
})

});