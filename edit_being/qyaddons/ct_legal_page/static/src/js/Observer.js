$(function(){

    $('#signup_tabs a').click(function (e) {

      e.preventDefault()

      $(this).tab('show')
    })

   var  MutationObserver = window.MutationObserver || window.WebKitMutationObserver || window.MozMutationObserver,

   		active = "active",

   		content = $("#template"),

   		signup = $("#signup_tabs"),

   		ObRemove = function(node){

   			$.each(node,function(){

				var hashId = $(this).find("a").attr("href"),

					hashPrev = ($(hashId).prev().length?$(hashId).prev():$(hashId).next());

				signup.find("li a[href='#"+hashPrev.attr("id")+"']").parent().addClass(active).siblings().removeClass(active);

				hashPrev.addClass(active).siblings().removeClass(active).end().end().empty().remove();

			})

   		},

   		ObAdd = function(node,SigActive){

   			$.each(node,function(){

   				var Now = Date.now(),

   					that = this,

   					hashId = $(SigActive).find("a").attr("href"),

   					clone = content.clone(true,true).addClass(active).attr("id",Now);

   				$(this).find("a").attr("href","#"+Now).end().addClass(active).siblings().removeClass(active);

   				$(hashId).after(content.clone(true,true).addClass(active).attr("id",Now)).next().siblings().removeClass(active);

   				new MutationObserver(function(mutations,observer){

   					mutations.map(function(record){

   						var NewNode = record.addedNodes;

   						if(NewNode.length && NewNode[0].nodeName=="DIV"){

   							$(NewNode).remove();

   						}

   					});

   				}).observe($(this).find("a").get(0),{
			   		childList:true	
			   	})

   			})

   		};

   		MutationObserver && new MutationObserver(function(mutations,observer){

		mutations.map(function(record){

			var SigAdd = record.addedNodes,

				SigRemove = record.removedNodes,

				SigActive = record.previousSibling.nodeType==1?record.previousSibling:record.nextSibling;
				


	        if(SigAdd.length){

	        	ObAdd(SigAdd,SigActive)
	        }

	        if(SigRemove.length){

	        	ObRemove(SigRemove,SigActive)
	        }

	    });

	}).observe(signup.get(0),{

   		childList:true	
   	});

})