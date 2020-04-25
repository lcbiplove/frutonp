var showPop = Pop.showPop;
var hidePop = Pop.hidePop;
var popShown = Pop.popShown;
var uid = Post.uid;
var comment_area = $("#write-comment-txtarea");
var reply_area = $("#reply-txtarea");
var reply_box = $("#reply-inpt-box");

var load_circle = Pop.load_circle;
var load_elips = Pop.load_elips;
var new_cmnt_count = 0;
function showTextArea(){
    comment_area.css({"height": "auto"});
    $("#comment-btn").removeAttr("disabled");
    $("#comment-btn").css("display", "inline");
}
function hideTextArea(){
    comment_area.css({"height": "34px"});
    $("#comment-btn").attr('disabled', '');
    $("#comment-btn").css("display", "none");
}
function commentMenuClicked(e){
    if(e.target.className == "comment-menu" || $(e.target).parent(".comment-menu").length)
        return true;
    return false;
}
function commentEditOpen(){
    return !(($("#cancel-edit").hasClass("d-none")));
}
function showDeleteDialog(){
    $("#chx0dmxd").html('<div class="real-modal"><div class="real-modal-container" tabindex="0"><div class="real-modal-header" style="background-color: #ff4a4a;"><div>Delete</div><div class="real-modal-close">&times;</div></div><div class="real-modal-body" style="padding: 10px 10px 10px 20px;">Are you sure you want to delete?</div><div class="modal-del-options"><button id="del-yes">Yes</button><button class="real-modal-close" id="del-no">No</button></div></div></div>');
    showPop();
}
function deleteConfirmation(e){
    return e.target.id=="del-yes" ? true : false;
}
function isReplyOpened(){
    return reply_box.css("display")=="flex" ? true : false;
}

function startSocket(websocketServerLocation=window.location, sec=5000){
    var protoc = "ws://";
    if(websocketServerLocation.protocol == "https"){
        protoc = "wss://";
    }
    var websocketServerLocation = protoc+websocketServerLocation.host+websocketServerLocation.pathname;
    var socket = new WebSocket(websocketServerLocation);
    
    socket.onopen = function(e){
        console.log("Post Opened");
    }

    socket.onmessage = function(e){
        json = JSON.parse(e.data);
        if(json.desc == "comment_added" && json.me != uid){
            new_cmnt_count++;
            if(new_cmnt_count == 1){
                $("#new-comments").html(`<span>${new_cmnt_count}</span> New Comment`);
            } else {
                $("#new-comments").html(`<span>${new_cmnt_count}</span> New Comments`);
            }
            $("#new-comments").addClass("new-comments-p");
        }
        else if(json.desc == "comment_delete" && json.me != uid){
            var del_div = $(`.show-reply[data-cm-id="${json.cm_id}"]`).closest("div.comment-of");
            del_div.css({"opacity": "0.35", "pointer-events": "none", "user-select": "none"});
            del_div.click(function(){return false;});
        }
        else if(json.desc == "comment_edit" && json.me != uid){
            var edit_div = $(`.show-reply[data-cm-id="${json.cm_id}"]`).closest("div").prev("div").children("span:nth-child(2)").html(json.editted_text);
        }
        else if(json.desc == "reply_added" && json.me != uid){
            var new_reply_div = $(`.show-reply[data-cm-id="${json.cm_id}"]`).closest("div").next("div.replies-cont");
            if(new_reply_div.children("p.more-replies").length == 0){
                new_reply_div.prepend(`<p class="more-replies" data-cm-id="${json.cm_id}&_&_1">New Reply (+1)</p>`);
            } 
            else {
                var new_reply_para = new_reply_div.children("p.more-replies");
                var arr__ = new_reply_para.attr("data-cm-id").split("&_");
                reply_count=arr__[2];
                reply_count++;
                new_reply_para.removeAttr("class").attr({"data-cm-id": `${json.cm_id}&_${arr__[1]}&_${reply_count}`, "class": "more-replies"}).html(`${arr__[1]} More Replies (+${reply_count})`);
            }
        }
        else if(json.desc == "reply_delete" && json.me != uid){
            var del_reply_div = $(`span.time-diff[data-rp-id="${json.rp_id}"]`).closest("div.reply-of");
            del_reply_div.css({"opacity": "0.35", "pointer-events": "none", "user-select": "none"});
            del_reply_div.click(function(){return false;});
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
socket = startSocket();


/*  */
comment_area.on("focus", function(){
    $(this).attr("rows", "3");
});
comment_area.on("blur", function(){
    if(comment_area.val() === ""){
        $(this).attr("rows", "1");
    }                   
});
comment_area.keyup(function(){
    if($(this).val().trim().length >= 1){
        showTextArea();
    } else {
        hideTextArea();
    }
});

/**Comment menu clicked */
$("#comments").on("click", ".comment-menu", function(e){
    var cm_id = $(this).data("cm-id");
    $("#edit-cm").attr("data-cm-id", cm_id);
    $("#upload-rm-pp").attr("data-cm-id", cm_id);
    $("#chx0dmxd").html(`<div class="real-modal"><div class="real-div-container back-trans">${load_elips}</div></div`);
    showPop();
    $("#chx0dmxd").load('comment-option/'+cm_id+'/', function(response, status, xhr){
        if(status == 'success'){
            showPop();
        } else {
            $("#chx0dmxd").html(``);
        }
    });     
});

/** If edit button on comment is clicked */
$("#chx0dmxd").on("click", "#edit-cm", function(){
    cm_id = $(this).data("cm-id");
    var text = $(`.comment-menu[data-cm-id='${cm_id}']`).closest("div").prev("div").children(".act-com-text").text();
    hidePop();
    $('html, body').animate({scrollTop: comment_area.offset().top}, 1000, function(){
        comment_area.val(text);
    });
    showTextArea();
    comment_area.focus();
    comment_area.attr("placeholder", "Enter edits..");
    $("#cancel-edit").removeClass("d-none");
    $("#comment-btn").text("Save edit");       
});

/** If delete button on comment is clicked, Delete comment */
$("#chx0dmxd").on("click", "#upload-rm-pp", function(e){
    cm_id = $(this).data("cm-id");
    showDeleteDialog();
    e.stopPropagation();
    $("#del-yes").on("click", function(e){        
        $(".real-modal-container").addClass("back-trans fl-mid").html(load_elips);
        var response = $.ajax({
            type: "POST",
            url: `del-comment/${cm_id}/`,
            data: {
                'csrfmiddlewaretoken': Post.csrf,
                'cm_id': cm_id
            }
        });
        response.done(function(result){
            hidePop();
            socket.send(JSON.stringify({"desc": "comment_delete", "cm_id": cm_id}));

            var edit_div = $(`.comment-menu[data-cm-id='${cm_id}']`).closest(".comment-of");
            $('html, body').animate({scrollTop: (edit_div.offset().top-55)}, 500, function(){
                edit_div.css("background-color", "#07C044");
                edit_div.fadeOut(1000, 'linear', function(){
                    this.remove();
                    if(!($('.comment-of').length)){
                        $("#comments").html('<div class="comment-of no-comment">No Comments</div>');
                    }
                });
                $("#chx0dmxd").html('');
            });
        });
        response.fail(function(xhr, status, error){
            hidePop();
            console.log(`${xhr.status} ${status} (${error})`);
        });

    });
});

$("#comment-btn").on("click", function(){
    var comment = comment_area.val();
    comment = comment.trim();
    try{
        cm_id = $("#edit-cm").data("cm-id");
    } catch{
        cm_id = null;
    }
    if(comment.length !== 0){
        var data = {
            'comment': comment,
            'csrfmiddlewaretoken': Post.csrf
        }
        if(commentEditOpen() && cm_id !== null){
            data['cm_id'] = cm_id;
        }
        var response = $.ajax({
            type: "POST",
            url: "add-comment/",
            data: data
        });
        $("#cancel-edit").trigger("click");
        $("#comment-btn").attr("disabled");
        response.done(function(result){
            if(result.status == true){
                comment_id = result.id;
                /* If edit */
                if(result.edit == true){
                    socket.send(JSON.stringify({"desc": "comment_edit", "cm_id": comment_id, "editted_text": result.text}));

                    var edit_div = $(`.comment-menu[data-cm-id='${cm_id}']`).closest(".comment-of");
                    $('html, body').animate({scrollTop: (edit_div.offset().top-55)}, 1000, function(){
                        edit_div.load('added-comment/'+comment_id+'/');
                    });
                } else {
                    socket.send(JSON.stringify({"desc": "comment_added", "cm_id": comment_id}));

                    $.get('added-comment/'+comment_id+'/', function(data){ 
                        if($(".comment-of").hasClass('no-comment')){
                            $(".comment-of").hide();
                        }
                        $(".comment-of").last().after(data);
                    });
                }                    
            }
        });
    }
});

$(document).on("click", function(e){
    if(e.target.className !== "comment-menu" && !commentMenuClicked(e) && e.target.id !== "del-yes" )
        if($(e.target).parents(".real-modal-container").length == 0 || e.target.className == "real-modal-close" || e.target.className == "real-modal-close rm-rl-cl-dwn")
            if(popShown)
                hidePop();
});    

$("#cancel-edit").click(function(){
    $(this).attr("class", "d-none");
    comment_area.val('');
    $("#comment-btn").text("Comment");
    comment_area.attr("placeholder", "Add a comment..");
    $("#chx0dmxd").html('');
    hideTextArea();
});
/** Load new comments */
$("#new-comments").on("click", function(){
    var last_cm_id = $("#comments .comment-of").last().children(".w-100").children("div:nth-child(2)").children("span:nth-child(2)").children("a.show-reply").data("cm-id");
    try{
        last_cm_id = parseInt(last_cm_id);
        new_cmnt_count = 0;
        $(this).removeClass("new-comments-p").html("");
        $.get(`new-comments/${last_cm_id}/`, function (data, textStatus, jqXHR){
                $("#comments .comment-of").last().after(data);
            }
        );
    } catch (e){}
});



/* Show reply input box on reply click */
$("#comments").on("click", ".show-reply", function(){
    cm_id = $(this).attr("data-cm-id");
    html_of_reply = $(this).html();

    if(isReplyOpened()){
        $(".show-reply").html("Reply");
    }
    if(html_of_reply == "Reply"){
        $(this).closest("div").next(".replies-cont").append(reply_box);
        $("#reply-btn").attr('data-cm-id', cm_id);
        reply_box.css("display", "flex");
        reply_area.focus();
        $(this).html("Hide");
    } else {
        reply_box.hide("fast");
        $(this).html("Reply");
    }
});
reply_area.keyup(function(){
    if($(this).val().length >= 1){
        $("#reply-btn").removeAttr("disabled");
    } else {
        $("#reply-btn").attr("disabled", "");
    }

    if($(this).val().length >= 50){
        $("#reply-btn").css({"padding": "23px 5px", "bottom": "0px"});
        $(this).css({"height": "auto"});
        $(this).attr("rows", "3");
    } else {
        $("#reply-btn").css({"padding": "8px 5px", "bottom": "9px"});
        $(this).css({"height": "31px"});
        $(this).attr("rows", "1");
    }
});
/* Reply clicked */
$("#reply-btn").click(function(){
    reply_btn = $(this);
    cm_id = $(this).attr("data-cm-id");
    var data = {
        'csrfmiddlewaretoken': Post.csrf,
        'cm_id': cm_id,
        'reply': reply_area.val()
    }
    var response = $.ajax({
                    type: "POST",
                    url: `comment/${cm_id}/add-reply/`,
                    data: data
                });
    $(this).attr("disabled", "disabled");
    response.done(function(result){
        rp_id = result.id;
        if(typeof cm_id === "undefined"){
            cm_id=99;
        }
        socket.send(JSON.stringify({"desc": "reply_added", "cm_id": cm_id, "rp_id": rp_id}));

        $.get(`comment/${cm_id}/added-reply/${rp_id}/`, function(data){
            var reply_div_of_new = reply_btn.parents("div.reply-inpt-box").prev("div.replies-in");
            if(reply_div_of_new.html().trim().length == 0){
                reply_div_of_new.html(data);
            } else {
                reply_div_of_new.children("div.reply-of").last().after(data);
            }
            reply_div_of_new.animate({scrollTop: reply_div_of_new.prop("scrollHeight")}, 500);
        });
        reply_area.val("");
        reply_box.hide("fast");
        $(".show-reply").html("Reply");
    });
    response.fail(function(xhr, status, error){
        reply_btn.removeAttr("disabled");
    });
});

/* View replies on click, New repliess */
$("#comments").on("click", ".more-replies", function(){
    var reply_p = $(this);
    var data_cm_id = $(this).attr("data-cm-id").split("&_");
    var cm_id = data_cm_id[0]; 
    if($(this).hasClass("showing")){
        reply_p.html(`Show replies`);
        reply_p.next("div.replies-in").children("div.reply-of").slice(0, -2).hide();
        reply_p.removeClass("showing").addClass("shown");
    }
    else if($(this).hasClass("shown")) {
        reply_p.html(`Hide replies`);
        reply_p.removeClass("shown").addClass("showing");
        reply_p.next("div.replies-in").children("div.reply-of").show();
    }
    else {
        var response = $.get(`comment/${cm_id}/view-replies/`);
        response.done(function(data){
            reply_p.next(".replies-in").html(data);
            reply_p.addClass("showing");
            reply_p.html("Hide replies");
            if(reply_p.next(".replies-in").children(".reply-of").length <= 2){
                reply_p.remove();
            }
            reply_p.attr("data-cm-id", `${data_cm_id[0]}&_${parseInt(data_cm_id[1])+parseInt(data_cm_id[2])}&_0`);
        });
        reply_p.html('<span class="load-cic"><span style="width: 0.85em; height: 0.85em;"></span></span>');
        response.fail(function(xhr, status, error){
            reply_p.children(".load-cic").remove();
        });
    }
});

/**Delete replies */
$(".replies-cont").on("click", ".rpl-del", function(e){
    var del_btn = $(this);
    var rp_id = del_btn.data("rp-id");
    var deleting_box = del_btn.parents("div.reply-of");
    var cm_id = deleting_box.parents("div.replies-cont").prev("div").children("span").eq(1).children("a.show-reply").data("cm-id");
    showDeleteDialog();
    e.stopPropagation();
    $("#del-yes").on("click", function(e){
        $(".real-modal-container").addClass("back-trans").html(load_circle);
        var response = $.ajax({
            type: "POST",
            url: `comment/${cm_id}/del-reply/${rp_id}/`,
            data: {
                'csrfmiddlewaretoken': Post.csrf,
                'cm_id': cm_id,
                'rp_id': rp_id
            }
        });
        response.done(function(result){
            hidePop();
            socket.send(JSON.stringify({"desc": "reply_delete", "cm_id": cm_id, "rp_id": rp_id}));

            deleting_box.parents("div.replies-in").animate({scrollTop: deleting_box.prev().prop("scrollHeight")}, 500, function(){
                deleting_box.css("background-color", "#07C044");
                deleting_box.fadeOut(1000, 'linear', function(){
                    this.remove();
                });
                $("#chx0dmxd").html('');
            });
        });
        response.fail(function(xhr, status, error){
            console.log(`${xhr.status} ${status} (${error})`);
        });
    });
});


/** Text area scroll */
$(function() {  
    comment_area.niceScroll({cursorcolor: '#ffa500', railalign: 'left'});
    reply_area.niceScroll({cursorcolor: '#ffa500', railalign: 'left'});
    if(!(navigator.userAgent.match(/Android/i)||navigator.userAgent.match(/webOS/i)||navigator.userAgent.match(/iPhone/i)||navigator.userAgent.match(/iPad/i)||navigator.userAgent.match(/iPod/i)||navigator.userAgent.match(/BlackBerry/i))){
        $(".replies-in").niceScroll({cursorwidth: "8px", cursorcolor: "#bbb"});
    }
});