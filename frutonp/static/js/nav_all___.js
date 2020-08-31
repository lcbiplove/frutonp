heightFromTop = $(this).scrollTop();

$("#sort-by-select").val($("#sort-by-select").attr("value"));

if(heightFromTop > 10){
    $('.nav-bar').addClass("nav-reduced");
} else {
    $('.nav-bar').removeClass("nav-reduced");
}

$(window).scroll(function(){
    heightFromTop = $(this).scrollTop();
    if(heightFromTop > 10){
        $('.nav-bar').addClass("nav-reduced");
    } else {
        $('.nav-bar').removeClass("nav-reduced");
    }
});

navIsOpen = false;
/* Settings open and close */
function showSet(){
    $(".set-cont").css({"display": "block"});
    $("#t-up").removeClass("fa-sort-down");
    $("#t-up").addClass("fa-sort-up");
    $("#t-up").css("margin-top", "5px");
}
function hideSet(){
    $(".set-cont").css({"display": "none"});
    $("#t-up").removeClass("fa-sort-up");
    $("#t-up").addClass("fa-sort-down");
    $("#t-up").css("margin-top", "0");
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
    $("#mb-srch-icon").addClass("mb-srch-open");
    $(".mb-srch-n-sel").css("display", "block");
    $(".set-not-btn").css("display", "none");
    $("#menu-btn").css("display", "none");
    $("#mb-srch-inpt").focus();
}
function closeMbSearch(){
    $("#mb-srch-icon").removeClass("mb-srch-open");
    
    $(".mb-srch-n-sel").css({"display": "none"});
    $(".set-not-btn").css("display", "flex");
    $("#menu-btn").css("display", "block");
    $("body").removeClass("o-hidden");
    $(".srch-overlay").addClass("d-none");
    $(".nav-bar").removeClass("pad-3");
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
        if(!$("#mb-srch-icon").hasClass("mb-srch-open")){
            openMbSearch();
        } else {
            fullButNoFocus();
        }
    }
    else if(!$(e.target).parents(".mb-side-bar").length) {
        if($("#mb-srch-icon").hasClass("mb-srch-open")){
            closeMbSearch();
        }
    }
    if(e.target.className == "mb-srch-select") {
        fullButNoFocus();
    }
});

$(".srch-form").on("submit", function(e){
    $(this).children("input[type=search]").attr("name", "");
    $(this).children("input[type=search]").val();
    $(this).attr("action", `/search/${$(this).children("input[type=search]").val()}`);
});

$("#sort-by-select").on("change", function(){
    active_tab = $(".srch-tab-active").html();
    active_tab = active_tab.toLowerCase();
    active_tab = active_tab.indexOf("s", active_tab.length-1) == -1 ? active_tab : active_tab.substring(0, active_tab.length-1)
    console.log(window.location.replace(window.location.href.split('?')[0]+`?tab=${active_tab}&sort-by=${$(this).val()}`));
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

$("header").on("click", ".mb-srch-open", function(){
    $("#mb-srch-form").submit();
});

$("#mb-srch-inpt").on("focus", function(){
    $("body").addClass("o-hidden");
    $(".srch-overlay").removeClass("d-none");
    $(".nav-bar").addClass("pad-3");
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