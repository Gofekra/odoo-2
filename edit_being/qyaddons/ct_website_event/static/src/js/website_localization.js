odoo.define("cotong_im_chat",function(require){

	var ajax = require('web.ajax');

    var href = window.location.href;

    if(href.indexOf("event")>=0 && href.indexOf("register")>=0){

    var cKey = href.match(/-(\d*)\//)[1];

    function setCookie(name, value, iDay){

        var oDate = new Date();

            oDate.setHours(0);

            oDate.setMinutes(0);

            oDate.setSeconds(0);

        oDate.setDate(oDate.getDate()+iDay);

        document.cookie=name+'='+value+';expires='+oDate+';path=/';

    }

    function getCookie(name){

        var arr = document.cookie.split('; ');

        for(var i=0;i<arr.length;i++){

            var arr2=arr[i].split('=');

            if(arr2[0]==name){

                return arr2[1];

            }

        }

        return '';
    }

    function removeCookie(name){

        setCookie(name, 1, -1);
    }

    ajax.jsonRpc("/website/get_user_info", 'call', []).then(function(result){

        odoo.uid = result.id

    });

    var host = window.location.hash.split("#");

        host.shift();

        host = $.extend.apply($,host.map(function(result){

            var obj = {},

                result  = result.split("-");

                obj[result[0]] = result[1];

                return obj;
        }));

        if(host.jtss && !getCookie('key'+host.jtss+host.uid+cKey)){

            $.getJSON('http://ip.chinaz.com/getip.aspx?type=ip&output=json&callback=?&_='+Math.random(), function(data){  

                ajax.jsonRpc("/website/create_user_info", 'call', $.extend({id:cKey},host,data)).then(function(){

                    removeCookie("inherit_id");

                    setCookie("inherit_id",host.uid,1);

                    setCookie('key'+host.jtss+host.uid+cKey,1,1);
                
                })

            });   

        }


    }

})