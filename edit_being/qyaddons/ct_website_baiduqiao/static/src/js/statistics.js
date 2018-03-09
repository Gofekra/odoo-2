odoo.define('website.statistics', function (require) {

	  var ajax = require('web.ajax');

    var _hmt = _hmt || [];
    (function() {
      var hm = document.createElement("script");
      hm.src = "https://hm.baidu.com/hm.js?fd0eded3c143850eea30318a032a6e08";
      var s = document.getElementsByTagName("script")[0]; 
      s.parentNode.insertBefore(hm, s);
    })();

  	window.addEventListener("popstate", function() {
        _hmt.push(['_setAutoPageview', false]);
        _hmt.push(['_trackPageview', location.href.toString().replace(new RegExp(location.origin),"")]);                
    });
})