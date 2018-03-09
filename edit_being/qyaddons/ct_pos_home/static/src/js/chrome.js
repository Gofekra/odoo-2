odoo.define('ct_point_of_sale.chrome', function (require) {
"use strict";
	
	var Model = require('web.Model');
	var point_of_sale = require('point_of_sale.chrome');

	point_of_sale.Chrome.include({

		replace_crashmanager:function(){

			var self = this;

			this._super.apply(this, arguments);

			this.load_modules();
		},
		load_modules:function(){

			var model = new Model("res.users"),

            self = this;

            model.call("search_theme").then(function(enable) {

        		if(enable){

        			model.call("setup_theme",{
        				enable:[enable.split(".")[1]],
        				disable:['ct_theme_default','ct_theme_blue','ct_theme_palm','ct_theme_deepblue','ct_theme_green'],
        				get_bundle: true
        			}).then(function(bundleHTML) {

	                var $links = $('link[href*="point_of_sale.assets"]');

	                var $newLinks = $(bundleHTML).filter('link');

	                var nbLoaded = 0;

	                $newLinks.on('load', function (e) {

	                    $links.remove();

	                });

	                $newLinks.on('error', function (e) {

	                    linksLoaded.reject();

	                    window.location.hash = "theme=true";

	                    window.location.reload();

	                });

	                $links.last().after($newLinks);

        			})
        		}
        	})

            
		}
	})

})