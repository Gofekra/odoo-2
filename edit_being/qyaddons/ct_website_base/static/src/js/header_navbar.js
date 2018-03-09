$(function(){
	// 头部的nav点击事件
    $("#top_menu > li.dropdown").on("click",function(){

        $(this).find(".dropdown-menu").slideToggle("fast").parent().siblings("li.dropdown").find(".dropdown-menu").slideUp("fast");
    }) 
    
})
   
