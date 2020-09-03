var screen_height = MyScreen.height;
var screen_width = MyScreen.width
var load_circle = Pop.load_circle;
var load_elips = Pop.load_elips;
var csrf = $("#prfl_base_csrf").val();
var notif_wait_scroll;
var notif_page;

function startSocket(websocketServerLocation=window.location, sec=5000){
    var protoc = "ws://";
    if(websocketServerLocation.protocol == "https"){
        protoc = "wss://";
    }
    var websocketServerLocation = protoc+websocketServerLocation.host+"/home/";
    var socket = new WebSocket(websocketServerLocation);
    
    socket.onopen = function(e){
        //console.log("Notification Opened");
    }

    socket.onmessage = function(e){
        json = JSON.parse(e.data);
        if(json.new_notif == true){
            var innerTitle = $("title").html().split(") ");
            if(json.num !== 0){
                $("#notif-num").attr("class","").addClass("notif-num-yes").html(json.num);
                if(innerTitle.length == 1){
                    $("title").prepend(`(${json.num}) `);
                } else {
                    $("title").html(`(${json.num}) ${innerTitle[1]}`);
                }
            }
        }
    }

    socket.onerror = function (e) {
        console.log("Error", e)
    }
    socket.onclose = function(){
        // Try to reconnect in 5 seconds
        setTimeout(function(){startSocket()}, sec);
    }
    return socket;
}
notif_socket = startSocket();

function showNotif(){
    notif_wait_scroll = false;
    notif_page = 1;
    var addHeight = screen_height - $(".nav-bar").outerHeight();
    if(!$('.nav-bar').hasClass("nav-reduced")){
        addHeight += 6;
    }
    $("body").css("overflow", "hidden");
    $("#notificaion-cont").css({"height": `${addHeight}px`});
    if(screen_width <= 420){
        $(".notif-cont").css({"right": "-48px"});
        $("#ar-o-notif").css({"right": "65px"});
        $("#notificaion-cont").css({"height": `${addHeight}px`, "width": `${screen_width}px`});
    } 
    $(".notif-cont").css({"display": "block"});
    $("#t-up-notif").removeClass("fa-sort-down");
    $("#t-up-notif").addClass("fa-sort-up");
    $("#t-up-notif").css("margin-top", "5px");
    loadNotifs();
}
function hideNotif(){
    $("body").removeAttr("style");
    $(".notif-cont").css({"display": "none"});
    $("#t-up-notif").removeClass("fa-sort-up");
    $("#t-up-notif").addClass("fa-sort-down");
    $("#t-up-notif").css("margin-top", "0px");
}
function notifClick(){
    if($("#t-up-notif").hasClass("fa-sort-down")){
        showNotif();
    } else {
        hideNotif();
    }
}
function loadNotifs(){
    
    var req = $.ajax({
        url: '/home/show-notif/',
        type: 'POST',
        headers:{
            "X-CSRFToken": csrf
        },
        data: {
            'data': 'foo-data'
        }
    });
    $("#notificaion-cont").html(`<li class='fl-mid w-100 h-100'><span class="my-load"><span></span></span></li>`);
    req.done(function(response){
        var num = 0;
        if($("#notif-num").hasClass("notif-num-yes")){
            var innerTitle = $("title").html();
            num = parseInt(innerTitle.split(") ")[0].split("(")[1]);
            $("#notif-num").removeClass("notif-num-yes").addClass("notif-num-no").html("");
            $("title").html(innerTitle.split(") ")[1]);
        }
        $("#notificaion-cont").html(response);
        for(var ind=1; ind<=num; ind++){
            $(`#notificaion-cont li:nth-child(${ind})`).addClass('recent-notif');
        }
    });
}

$(document).on("click", function(e){
    // For notifications
    if($(e.target).parent("#notif-btn").length || e.target.id == "notif-btn"){
        notifClick();
    } 
    else if(!$(e.target).parents(".notif-cont").length){
        hideNotif();
    } 
});

$(document).on('click', '#notificaion-cont a', function(e) {
    NProgress.start();
    e.preventDefault();
    var href = $(this).attr("href");
    var notif_id = $(this).attr("data-notif-id");
    var req = $.ajax({
        url: `/home/notif-seen/${notif_id}/`,
        type: 'POST',
        headers:{
            "X-CSRFToken": csrf
        },
        data: {
            'data': 'foo-data'
        }
    });
    req.done(function(response){
        if(response.success == true){
            NProgress.done();
            window.location.href = href;
        }
    });
});

$("#notificaion-cont").on("scroll", function(){
    if(($(this).scrollTop() + $(this).innerHeight() >= $(this)[0].scrollHeight) && !notif_wait_scroll) {
        console.log('Hi');
        notif_wait_scroll = true;
        notif_page++;
        // $("#post-content ol").after("<span class='load-cic'><span style='background-color: #888; height: 1.8rem; width: 2rem;'></span></span>");
        var req = $.ajax({
            url: `/home/show-notif/?page=${notif_page}`,
            type: 'POST',
            headers:{
                "X-CSRFToken": csrf
            },
            data: {
                'data': 'foo-data'
            }
        });
        $("#notificaion-cont").append('<li class="fl-mid loading-more-notif"><span class="my-small-load"><span></span></span></li>');
        req.done(function(response){
            $("li.loading-more-notif").remove();
            if(response.finished == true){
                notif_wait_scroll = true;
            } else {
                notif_wait_scroll = false;
                $("#notificaion-cont").append(response);
            }
        });
        req.fail(function(){
            notif_wait_scroll = false;
        });

    }
});