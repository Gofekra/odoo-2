odoo.define('web_enterprise.BackEndMenu', function (require) {
"use strict";

  var ajax = require('web.ajax');
  var config = require('web.config');
  var core = require('web.core');
  var Widget = require('web.Widget');
  var base = require('web_editor.base');

  setTimeout(function(){
    
  },1000)
var mySwiper = function(element,size,config){

   return new Swiper(element,

     ($.extend({},{

     slidesPerView : size,

     spaceBetween : 0,

     freeMode : true,

     freeModeSticky : true,

     preventClicks : true,//阻止点击

     prevButton:'.swiper-button-prev',
     
     nextButton:'.swiper-button-next'

     },config || {}))

     );
}

//个数少时提供占位
var MenuPerch = function(element,size){

  var ele = $(element),

      child = ele.children(),

      childFirst = child.last().clone().empty().addClass('PerchHide'),

      childSize = child.size(),

      style=String();


      if(childSize>=size){

        return;

      };

      style = "\
      <style scoped>\
        .PerchHide{\
          width:"+childFirst.width()*(size-childSize)/2+"px !important\
        }\
      </style>\
      ";

      ele.prepend(childFirst).parent().before(style);
      
}

var selectEvent = function(element){

  var Dom  = $(element),

  hove = function(){

      if($(this).closest("div").hasClass('active')){

        return false;

      }

      var hover = $(this).attr("src");

      $(this).attr("src",$(this).data('hover')).data('hover',hover);

  }

  Dom.hover(hove,hove).click(function(){

    hove.call($(this).closest("div").addClass('active').siblings().filter('.active').removeClass('active').find(element));

  });

}

var IponeMove = function(element){

  var aImg = $(element);

  var aWidth = [];

  var i;

  //保存原宽度, 并设置当前宽度

  aImg.each(function(i,val){

     aWidth.push($(this).width());

     $(this).width($(this).width()/2)

  });

    //鼠标移动事件
  $("document,body").on("mousemove",function(event){

    var event = event || window.event

    aImg.each(function(i){

      var a = event.clientX - $(this).get(0).getBoundingClientRect().left - $(this).width() / 2;

      var b = event.clientY - $(this).get(0).getBoundingClientRect().top - $(this).height() / 2;

      var iScale = 1 - Math.sqrt(a * a + b * b) / 250;

      if (iScale < 0.5) iScale = 0.5;

      $(this).width(aWidth[i] * iScale) ;

    })

  });

}

//PC界面滚轮菜单滑动
var onWhellEvent = function(facility,el){

  var AppSwitcher = el,TheEvent = "wheel";

  if(facility.versions.firefox){

    TheEvent = "DOMMouseScroll"

  }

  document.addEventListener(TheEvent, myFunction);

  function myFunction(event){

     var wheelDelta=event.wheelDelta || event.detail && event.detail*-1 || 0,

     DocHasClass = AppSwitcher.hasClass('active');

    if(wheelDelta>0){//向上滚动

      !DocHasClass || AppSwitcher.removeClass('active');

    }else{//向下滚动

      DocHasClass || AppSwitcher.addClass('active');
      
    }

  }

}

//手机触屏菜单滑动
var onTouchEvent = function(el){

    document.addEventListener('touchstart',touch, false);

    document.addEventListener('touchmove',touch, false);  

    var offset = 0,

    AppSwitcher = el;

    function touch (event){  

        var event = event || window.event;  
   
        switch(event.type){  

            case "touchstart": 

                offset = event.touches[0].clientY;
                
                break;  
  
            case "touchmove":  
               

                if(offset>event.touches[0].clientY){//往上滑

                   AppSwitcher.hasClass('active') || AppSwitcher.addClass('active');

                }else{//往下滑

                   !AppSwitcher.hasClass('active') || AppSwitcher.removeClass('active');

                }

                offset = event.touches[0].clientY;
                 
                break;  
        }  
           
    }  

}

var TouchOff = function(done,fail,always){

    var browser={

    versions:function(){

           var u = navigator.userAgent, app = navigator.appVersion;

           return {//移动终端浏览器版本信息

                trident: u.indexOf('Trident') > -1, //IE内核

                presto: u.indexOf('Presto') > -1, //opera内核

                webKit: u.indexOf('AppleWebKit') > -1, //苹果、谷歌内核

                firefox: u.indexOf("Firefox")>-1, //火狐内核

                mobile: !!u.match(/AppleWebKit.*Mobile.*/)||!!u.match(/AppleWebKit/), //是否为移动终端
                
                ios: !!u.match(/i[^;]+;( U;)? CPU.+Mac OS X/), //ios终端
                
                android: u.indexOf('Android') > -1 || u.indexOf('Linux') > -1, //android终端或者uc浏览器
                
                iPhone: u.indexOf('iPhone') > -1 || (u.indexOf('Mac') > -1 && u.indexOf('Macintosh') < 0), //是否为iPhone或者QQHD浏览器
                
                iPad: u.indexOf('iPad') > -1, //是否iPad
                
                webApp: u.indexOf('Safari') == -1 //是否web应该程序，没有头部与底部
            };

         }(),

         language:(navigator.browserLanguage || navigator.language).toLowerCase()
    }

    if (browser.versions.ios||browser.versions.android||browser.versions.iPhone||browser.versions.iPad) {

        done(browser);  

    }else{

        fail(browser);

    }
       always(browser);
}


  return Widget.extend({
      load:function(el){

        var el = el;

      TouchOff(function(facility){//手机
        mySwiper(el.find('#AppSwitcher-swiper .swiper-container'),5,{
          prevButton:'.Indexmenu-prev',
          nextButton:'.Indexmenu-next',
          observer: true,
          observeParents: true
        });
        MenuPerch(el.find('#AppSwitcher-swiper .swiper-container  .swiper-wrapper'),5);

        onTouchEvent(el.find('#AppSwitcher-swiper'));
        
        },function(facility){//电脑

            IponeMove(el.find('.TouchMove'));

            mySwiper(el.find('#AppSwitcher-swiper .swiper-container'),8,{
              prevButton:'.Indexmenu-prev',
              nextButton:'.Indexmenu-next',
              observer: true,
              observeParents: true
            });

            onWhellEvent(facility,el.find('#AppSwitcher-swiper'));

            MenuPerch(el.find('#AppSwitcher-swiper .swiper-container .swiper-wrapper'),8);

          },function(facility){//全部

            selectEvent(el.find('.TouchMove'));

            $(".o_content").ready(function($) {

              $(".o_content").scroll(function(){ $(this).find("thead").css("cssText","transform:translateY("+$(this).scrollTop()+"px)") })

            });
           
          });
      }
  })


});
