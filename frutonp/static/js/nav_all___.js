heightFromTop = $(this).scrollTop();
if(heightFromTop > 10){
    $('.nav-bar').css({"box-shadow": "3px 0px 5px #555", "padding": "3px 0px"});
} else {
    $('.nav-bar').css({"box-shadow": "none", "padding": "10px 0px"});
}

$(window).scroll(function(){
    heightFromTop = $(this).scrollTop();
    if(heightFromTop > 10){
        $('.nav-bar').css({"box-shadow": "3px 0px 6px #555", "padding": "3px 0px"});
    } else {
        $('.nav-bar').css({"box-shadow": "none", "padding": "10px 0px"});
    }
});

navIsOpen = false;
/* Settings open and close */
function showSet(){
    $(".set-cont").css({"display": "block"});
    $("#t-up").removeClass("fa-sort-down");
    $("#t-up").addClass("fa-sort-up");
    $("#t-up").css("top", "5px");
}
function hideSet(){
    $(".set-cont").css({"display": "none"});
    $("#t-up").removeClass("fa-sort-up");
    $("#t-up").addClass("fa-sort-down");
    $("#t-up").css("top", "2px");
}
function setClick(){
    if($("#t-up").hasClass("fa-sort-down")){
        showSet();
    } else {
        hideSet();
    }
}

/* Nav bar functions */
function showNav(){
    $(".side-bar").css({"width": "275px"});
    $("#menu-btn").css({"visibility": "hidden"});
    navIsOpen = true;
}
function hideNav(){
    $(".side-bar").css({"width": "0px"});
    $("#menu-btn").css({"visibility": "visible"});
    navIsOpen = false;
}
/* Mobile search functions */
function openMbSearch(){
    setTimeout(function(){
        $(".mb-srch-n-sel").css("display", "block");
        $(".set-not-btn").css("display", "none");
        $("#mb-srch-icon").css({"background-color": "rgb(7, 192, 68)", "padding": "9px 10px 8px 10px", "top": "-22px",});
        $("#mb-srch-icon").addClass("canSrchOn");
        $("#mb-srch-inpt").focus();
    }, 0);
}
function closeMbSearch(){
    $(".set-not-btn").css("display", "flex");
    $("#mb-srch-icon").css({"background-color": "initial", "padding": "3px", "top": "-14px", "left": "-23px"});
    $("#mb-srch-icon").removeAttr("class");

    setTimeout(function(){
        $(".mb-srch-n-sel").css("display", "none");
    }, 200);
}
function fullButNoFocus(){
    var width = $("#mb-srch-inpt").css("width");
    $("#mb-srch-inpt").css("width", width);
}
/* All on click.... Select actions and functions */
$(document).click(function(e){
    // For settings
    if($(e.target).parent("#settings-btn").length || e.target.id == "settings-btn"){
        setClick();
    } 
    else if(!$(e.target).parents(".set-cont").length){
        hideSet();
    } 
    // For language tab in settings
    if(e.target.id == "lang" || $(e.target).parent("#lang").length){
        $("#settings-cont").css("display", "none");
        $("#lang-cont").css("display", "block");
    }
    if(e.target.id == "lang-back-set" || $(e.target).parent("#lang-back-set").length){
        $("#settings-cont").css("display", "block");
        $("#lang-cont").css("display", "none");
    }
    // Ham menu button
    if(e.target.id == "menu-btn" || $(e.target).parent("#menu-btn").length){
        showNav();
    }
    else if(!$(e.target).parents(".side-bar").length || $(e.target).parent("#side-close").length || e.target.id == "side-close"){
        hideNav();
    } 
    // Search icon on nav
    if(e.target.id == "mb-srch-icon" || $(e.target).parent("#mb-srch-icon").length){
        if(!$("#mb-srch-icon").hasClass("canSrchOn")){
            openMbSearch();
        } else {
            fullButNoFocus();
        }
    }
    else if(!$(e.target).parents(".mb-side-bar").length) {
        closeMbSearch();
    }
    if(e.target.className == "mb-srch-select") {
        fullButNoFocus();
    }
});

$(window).resize(function(){
    if($(window).width() > 850){
        if(navIsOpen){
            hideNav();
            navIsOpen = true;
        }
    } else {
        if(navIsOpen){
            showNav();
        } else {
            hideNav();
        }
    }
});

/* Pop up */
Pop = {
    load_circle: '<span class="load-cic"><span style="background: #ddd;"></span></span>',
    load_elips: '<span class="load-ellipsis"><span></span><span></span><span></span><span></span></span>',
    showPop: function(){
                $("body").css({"overflow": "hidden"});
                $(".real-modal").css({"display": "flex"});
                setTimeout(function(){
                    $(".real-modal-container").show(100);
                }, 100);
            },
    hidePop: function hidePop(){
                $(".real-modal-container").hide(100, function(){
                    $(".real-modal").css("display", "none");
                    $("body").css("overflow", "");
                    $(this).removeClass("back-trans fl-mid");
                });
            },
    popShown: function popShown(){ 
                var attr = $("body").attr("style")
                if( attr === undefined || attr.length === 0)
                    return false;
                return true;
            }
};