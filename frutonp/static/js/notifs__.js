function startSocket(websocketServerLocation=window.location, sec=5000){
    var protoc = "ws://";
    if(websocketServerLocation.protocol == "https"){
        protoc = "wss://";
    }
    var websocketServerLocation = protoc+websocketServerLocation.host+"/home/";
    var socket = new WebSocket(websocketServerLocation);
    
    socket.onopen = function(e){
        console.log("Notification Opened");
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
    $(".notif-cont").css({"display": "block"});
    $("#t-up-notif").removeClass("fa-sort-down");
    $("#t-up-notif").addClass("fa-sort-up");
    $("#t-up-notif").css("margin-top", "5px");
}
function hideNotif(){
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

$(document).on("click", function(e){
    // For notifications
    if($(e.target).parent("#notif-btn").length || e.target.id == "notif-btn"){
        notifClick();
        if($("#notif-num").hasClass("notif-num-yes")){
            var innerTitle = $("title").html();
            $("#notif-num").removeClass("notif-num-yes").addClass("notif-num-no").html("");
            $.get("/home/reload-notif/",
                function (data, textStatus, jqXHR){}
            );
            $("title").html(innerTitle.split(") ")[1]);
        }
    } 
    else if(!$(e.target).parents(".notif-cont").length){
        hideNotif();
    } 
});

