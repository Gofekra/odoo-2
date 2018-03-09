$(function () {

    var module_client_width = document.body.clientWidth;
    //绑定滚动效果，向下滚动的时候追加class active
    $(window).scroll(function () {
        var scrolltop_height = $(window).scrollTop();

        if (scrolltop_height > 79) {
            if(module_client_width>768){
                $("#container-fluid").addClass("active");
            }

        } else {
            $("#container-fluid").removeClass("active");
        }
    })
    

        if ($("#container-fluid").hasClass("active")) {
            var li_dis = $(".module_nav").offset().left;
            if (li_dis > 125) {
                $("ul.module_nav li>a").css("padding", "5px 15px");
            } else {
                $("#wrapwrap .container-fluid.active").css({"width":"100%","text-align":"center"});
            }

    }

    //给单页面中产品介绍，点击它时候和下面的导航条的时候 保持它的状态
    //获取当前页面的url
    var url_w = window.location.href;
    var url_arrs = url_w.split('/');
    var urls = url_arrs[0] + "//" + url_arrs[2] + "/module";
    if (url_w.indexOf(urls) != -1) {
        $('a[href="/module"]').css({"background-color": "#69b0e7"});
        $('.module_nav li:first-child').css({"background-color": "#f38851", "color": "#fff"});
    }

    //判断当前页面url中是否有#(是否是子页面)，有的话切割字符串，取前面第一个数组元素，没有
    //的话就是最大页面
    if (url_w.indexOf('#') != -1) {
        var url_w_array = url_w.split("#");
        var url_w_array_i = url_w_array[0];
    }
    else if (url_w.indexOf('#') == -1) {
        var url_w_array_i = url_w;
    }
    var a_href = $("ul.module_nav li a");
    $('.module_nav li').css({"background-color": "rgba(255,255,2555,0.5)", "color": "#666"});

    //这里是点击12个导航条中a 标签时，产生的单页面的效果
    //网站是单页面，点击某个a标签时候，会跳到指定页面即刷新，因此，自己写的点击事件执行后会立即在刷新后失去效果
    //解决的办法就是，在它的框架上，点击a 时，会留下url,因此判断它的 url和a 的href 值是否相等，再追加样式
    for (var i = 0; i < a_href.length; i++) {
        if (a_href[i].href === url_w_array_i) {
            $(a_href[i]).css({"background-color": "#f38851", "color": "#fff", "border-radius": "5px"});
        } else {
            $(a_href[i]).css({"background-color": "transparent", "color": "#333"});
        }
    }
})
