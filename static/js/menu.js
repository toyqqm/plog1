$(".nav li").click(function(){
    $(this).siblings().find('a').removeClass("active").addClass("collapsed");
    $(this).siblings().find('div').removeClass("in").attr("aria-expanded","false");
});


