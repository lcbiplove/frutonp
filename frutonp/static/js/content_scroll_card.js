$(function(){
    setTimeout(function(){
        $(".veg-card-main").css({"overflow": "auto"});
    }, 1000);

    var veg_mb = $(".veg-name-price-mb");
    var veg_desk = $(".veg-name-price-desk");
    if ($(window).width() <= 600) {
        $(veg_mb).css("display", "block");
        $(veg_desk).css("display", "none");
    }  else {
        $(veg_mb).css("display", "none");
        $(veg_desk).css("display", "block");
    }
    $(window).resize(function(){
        if ($(window).width() <= 600) {
            $(veg_mb).css("display", "block");
            $(veg_desk).css("display", "none");
        }  else {
            $(veg_mb).css("display", "none");
            $(veg_desk).css("display", "block");
        }
    });
});