odoo.define('web_chatter_paste.summernote', function (require) {
'use strict';

var core = require('web.core');
require('summernote/summernote'); // wait that summernote is loaded

//////////////////////////////////////////////////////////////////////////////////////////////////////////
/* Summernote Lib (neek hack to make accessible: method and object) */

var eventHandler = $.summernote.eventHandler;

// override summernote clipboard functionality

eventHandler.modules.clipboard.attach = function(layoutInfo) {

    var $editable = layoutInfo.editable();

    var imgReader = function(item){

	var file = item.getAsFile(),

	reader = new FileReader(),

	dtd  = $.Deferred();

    reader.onload = function(e){

    	dtd.resolve(e.target.result)

    };

    reader.readAsDataURL(file);

    return dtd;

	}

    $editable.on('paste', function(e) {

        var paste,types,items,index,baseData,browser360= null,

		  	 include = ["text/plain", "text/html", "text/rtf", "Files"];

		  	if(window.clipboardData && clipboardData.setData) {

		  	 	 paste = window.clipboardData.items;

		  	}else{

		  	 	paste = (e.originalEvent || e).clipboardData;

		  	}

	  	 	if(!paste){

	  	 		return;

	  	 	}

	  	 	types = paste.types;

	 		items = paste.items;

	 		browser360 = paste.getData('text/yne-image-json');

	  	 	if(types.length==1 && types[0]==="text/plain"){

	  	 		e.preventDefault();

	  	 		document.execCommand('insertText', false,paste.getData('text/plain'));

	  	 	}else if(types.length==1 && types[0]==="Files"){

	  	 		e.preventDefault();

	  	 		if(items[0].kind==='file' && items[0].type.match(/^image/)){


	  	 			imgReader(items[0]).done(function(result){

	  	 				document.execCommand('insertImage', false,result);


	  	 			});

	  	 		}

	  	 	}else{

	  	 		if(include.indexOf(types[types.length-1])>-1){

	  	 			e.preventDefault();

	  	 			document.execCommand('insertHTML',false,paste.getData('text/html'));

	  	 		}else if(types.indexOf('text/html')>-1 && include.indexOf(types[types.length-1])==-1){

		  	 		baseData = browser360?JSON.parse(browser360):JSON.parse(types[types.length-2]);

		  	 		var imgReg = /<img [^>]*data-attr-org-src-id=['"]([^'"]+)[^>]*>/gim,

	  	 			imgsite = /src=['"]([^'"]+)['"]*/gim;

	  	 			if(Object.keys(baseData.data).length){

	  	 				e.preventDefault();

		  	 			document.execCommand('insertHTML',false,paste.getData('text/html').replace(imgReg,function(match,$1){

		  	 			return match.replace(imgsite,'src='+baseData.data[$1].base64);

		  	 			}));

	  	 			}

	  	 		}

	  	 	}
    });
};

});
