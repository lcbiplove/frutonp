// const MAX_POST_LOAD = 10;
// NumberTranslator.translateToNep('4');
const MAX_COMMENT = 24;
var showPop = Pop.showPop;
var hidePop = Pop.hidePop;
var popShown = Pop.popShown;
var uid = $("#uid").val();
var csrf = $("#csrf_token").val();
var comment_area = $("#write-comment-txtarea");
var reply_area = $("#reply-txtarea");
var reply_box = $("#reply-inpt-box");
var post_id = parseInt((window.location.pathname).split('/')[2]);  
var comment_id;
var reply_id;
var wait_scroll = false;    
var comment_loaded = 1;
var root_url = `/post/${post_id}`;

var load_circle = Pop.load_circle;
var load_elips = Pop.load_elips;
var post_edited_data;
var small_load = '<i class="fa fa-spinner small-load"></i>'
var new_cmnt_count = 0;

function manageTotalComments(plus_minus="-"){
    var total_cmnts = parseInt(NumberTranslator.translateToEng($("#total-cmnts").html()));
    plus_minus = plus_minus == "-" ? plus_minus = total_cmnts-1 : plus_minus = total_cmnts+1;
    if(plus_minus >= MAX_COMMENT){
        disableNewComment();
    } else {
        enableNewComment();
    }
    $("#total-cmnts").html(NumberTranslator.translateToNep(plus_minus));
}
function showTextArea(isEdit=false){
    comment_area.css({"height": "auto"});
    if($("#comment-btn").attr("data-disabled") == "false" || isEdit){
        $("#comment-btn").removeAttr("disabled");
    }
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
function showDeleteDialog(for_=null){
    var for_ = for_=="delete_post" ? pgettext("argument", "the post") : "";
    $("#chx0dmxd").html('<div class="real-modal"><div class="real-modal-container" tabindex="0"><div class="real-modal-header" style="background-color: #ff4a4a;"><div>'+gettext('Delete')+'</div><div class="real-modal-close">&times;</div></div><div class="real-modal-body" style="padding: 10px 10px 10px 20px;">'+gettext('Are you sure you want to delete')+ for_+'?</div><div class="modal-del-options"><button id="del-yes">'+gettext('Yes')+'</button><button class="real-modal-close" id="del-no">'+gettext('No')+'</button></div></div></div>');
    showPop();
}
function deleteConfirmation(e){
    return e.target.id=="del-yes" ? true : false;
}
function isReplyOpened(){
    return reply_box.css("display")=="flex" ? true : false;
}
function disableNewComment() {
    $("#comment-btn").attr("disabled", "");
    $("#comment-btn").attr("data-disabled", "true");
}
function enableNewComment() {
    $("#comment-btn").removeAttr("disabled");
    $("#comment-btn").attr("data-disabled", "false");
}
function errorMessageHandler(guess, sol, extra, timeout=20000){
    $(".act-guess").html(guess);
    $(".act-sol").html(sol ?? gettext("Try again or reload the page."));
    $(".act-extra").html(extra ?? gettext("Reload"));
    $(".act-div").css({"bottom": "0px"});
    setTimeout(function(){
        $(".act-div").css({"bottom": "-1000px"});
    }, timeout); 
}
function addCmmntMssgErrHandler(comment, edit_cm_id=null){
    if(edit_cm_id == null){
        errorMessageHandler(guess=gettext("Could not add comment."), sol=gettext("Try again!!!"), extra='');
        comment_area.val(comment);
        comment_area.focus();
        comment_area.trigger("keyup");
    } else {
        errorMessageHandler(guess=gettext("Could not edit comment."), sol=gettext("Try again!!!"), extra='');
        editComment(edit_cm_id);
    }
}
function editComment(cm_id){
    var text = $(`.comment-menu[data-cm-id='${cm_id}']`).closest("div").prev("div").children(".act-com-text").text();
    hidePop();
    $('html, body').animate({scrollTop: comment_area.offset().top}, 1000, function(){
        comment_area.val(text);
    });
    showTextArea(isEdit=true);
    comment_area.focus();
    comment_area.attr("placeholder", gettext("Enter edits.."));
    $("#cancel-edit").removeClass("d-none");
    $("#comment-btn").text(gettext("Save edit")); 
}
function showNewComment(new_cmnt_count){
    if(new_cmnt_count == 1){
        $("#new-comments").html('<span>'+NumberTranslator.translateToNep(new_cmnt_count)+' </span>'+ gettext('New Comment'));
    } else {
        $("#new-comments").html('<span>'+NumberTranslator.translateToNep(new_cmnt_count)+' </span>'+ gettext('New Comments'));
    }
    $("#new-comments").addClass("new-comments-p");
}
function viewReplies(cm_id){
    var new_reply_div = $(`.show-reply[data-cm-id="${cm_id}"]`).closest("div").next("div.replies-cont");
    if(new_reply_div.children("p.more-replies").length == 0){
        new_reply_div.prepend(`<p class="more-replies" data-cm-id="${cm_id}&_&_1">`+gettext('New Reply')+ `(+${NumberTranslator.translateToNep(1)})</p>`);
    } 
    else {
        var new_reply_para = new_reply_div.children("p.more-replies");
        var arr__ = new_reply_para.attr("data-cm-id").split("&_");
        reply_count=arr__[2];
        reply_count++;
        new_reply_para.removeAttr("class").attr({"data-cm-id": `${cm_id}&_${arr__[1]}&_${reply_count}`, "class": "more-replies"}).html(NumberTranslator.translateToNep(arr__[1]) +` ${gettext('More Replies')} (+`+NumberTranslator.translateToNep(reply_count)+')');
    }
}
function notificationGetter(){
    var url = window.location;
    var scroll_element;
    var split_by_slash = url.pathname.split('/');
    if(split_by_slash.length == 6 | split_by_slash.length == 5){
        NProgress.start();
        /** Post, comment, reply id */
        reply_id = parseInt(split_by_slash[4]);
        comment_id = parseInt(split_by_slash[3]);
        scroll_element = $(`a.show-reply[data-cm-id="${comment_id}"]`).closest('.comment-of');
        if(split_by_slash.length == 6){
            scroll_element = $(`span.time-diff[data-rp-id="${reply_id}"]`).closest("div.replies-in");
        }

        $(document).ready(function(){
            NProgress.done();
            $([document.documentElement, document.body]).animate({
                scrollTop: scroll_element.offset().top-$(".nav-bar").innerHeight()
            }, 1000, function(){
                if(split_by_slash.length == 6){
                    scroll_to_elem = $(`span.time-diff[data-rp-id="${reply_id}"]`).closest(".reply-of");
                    scroll_element.animate({
                        scrollTop: scroll_to_elem.offset().top - scroll_element.offset().top - scroll_element.height() + scroll_to_elem.height()
                    }, 500, function(){
                        scroll_to_elem.addClass('la-cm-of-pst');
                    });
                } else {
                    scroll_element.addClass('la-cm-of-pst');
                }
            });
        });
    } 
}

function startSocket(websocketServerLocation=window.location, sec=5000){
    var protoc = "ws://";
    if(websocketServerLocation.protocol == "https"){
        protoc = "wss://";
    }
    var websocketServerLocation = protoc+websocketServerLocation.host+websocketServerLocation.pathname;
    var socket = new WebSocket(websocketServerLocation);
    socket.onopen = function(e){
        //
    }

    socket.onmessage = function(e){
        json = JSON.parse(e.data);
        if(json.desc=="post_delete" && json.me != uid){
            $(".actual-content").css({"opacity": "0.35", "pointer-events": "none", "user-select": "none"});
        }
        else if(json.desc=="post_edit"){
            $(".post-edit-del").html('<span class="post-edited">'+gettext('Post Edited')+'</span>');
            post_edited_data = json.data;
        }
        else if(json.desc == "comment_added" && json.me != uid){
            new_cmnt_count++;
            if($(".comment-of").hasClass('no-comment')){
                $($(".comment-of.no-comment")).remove();
            }
            showNewComment(new_cmnt_count);
            manageTotalComments("+");
        }
        else if(json.desc == "comment_delete" && json.me != uid){
            manageTotalComments();
            var del_div = $(`.show-reply[data-cm-id="${json.cm_id}"]`).closest("div.comment-of");
            del_div.css({"opacity": "0.35", "pointer-events": "none", "user-select": "none"});
            del_div.click(function(){return false;});
        }
        else if(json.desc == "comment_edit" && json.me != uid){
            var edit_div = $(`.show-reply[data-cm-id="${json.cm_id}"]`).closest("div").prev("div").children("span:nth-child(2)").html(json.editted_text);
        }
        else if(json.desc == "reply_added" && json.me != uid){
            viewReplies(json.cm_id);
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

notificationGetter();


$(".post-edit-del").on("click", ".post-edited", function(){
    $(this).html(small_load);
    setTimeout(function(){
        for (const [key, value] of Object.entries(post_edited_data)) {
            if(key=="location"){
                if(value){
                    $(`#${key}`).html(value).removeClass("d-none").addClass("la-cm-of-pst d-in-block");
                } else {
                    $(`#${key}`).html(value).removeClass("d-in-block").addClass("la-cm-of-pst d-none");
                }
            }
            else if(key=="phone2"){
                if(value){
                    $(`#${key}`).html(value).parent("div").removeClass("d-none").addClass("la-cm-of-pst d-in-block");
                } else {
                    $(`#${key}`).html(value).parent("div").removeClass("d-in-block").addClass("la-cm-of-pst d-none");
                }
            }
            else if(key=="thumbnail"){
                $(`#${key}`).attr("src", `/media/${value}`).addClass("la-cm-of-pst");
                $('.photo').attr("src", `/media/${value}`).addClass("la-cm-of-pst");
            }
            else if(key == "foodType"){
                $(`#title`).html(value).addClass("la-cm-of-pst");
                $(`#${key}`).html(value).addClass("la-cm-of-pst");
            }
            else {
                $(`#${key}`).html(value).addClass("la-cm-of-pst");
            }
        }
        $(".post-edited").remove();
    }, 100);
}); 

$("#del-post").on("click", function(e){
    e.preventDefault();
    showDeleteDialog("delete_post");
    e.stopPropagation();
    $("#del-yes").on("click", function(e){  
        $(".real-modal-container").addClass("back-trans fl-mid").html(load_elips);
        var response = $.ajax({
            type: "POST",
            url: "/post/delete/",
            data: {
                'csrfmiddlewaretoken': csrf,
                'pid': post_id
            }
        });
        response.done(function(result){
            hidePop();
            if(result.status){
                $(".actual-content").css({"opacity": "0.35", "pointer-events": "none", "user-select": "none"});
                socket.send(JSON.stringify({"desc": "post_delete"}));
                $("#chx0dmxd").html('');
            }
        });
        response.fail(function(xhr, status, error){
            hidePop();
            if(xhr.status==404){
                errorMessageHandler(guess=gettext("Post might have been deleted already."));
            } else {
                errorMessageHandler(guess=gettext("Could not delete post."));
            }
        });
    });
});

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
        showTextArea(isEdit = commentEditOpen() ? true : false);
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
    $("#chx0dmxd").load(`${root_url}/comment-option/${cm_id}/`, function(response, status, xhr){
        if(status == 'success'){
            showPop();
        } else {
            $("#chx0dmxd").html("");
        }
    });     
});

/** If edit button on comment is clicked */
$("#chx0dmxd").on("click", "#edit-cm", function(){
    cm_id = $(this).data("cm-id");
    editComment(cm_id);      
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
            url: `${root_url}/del-comment/${cm_id}/`,
            data: {
                'csrfmiddlewaretoken': csrf,
                'cm_id': cm_id
            }
        });
        response.done(function(result){
            hidePop();
            socket.send(JSON.stringify({"desc": "comment_delete", "cm_id": cm_id}));
            manageTotalComments();

            var edit_div = $(`.comment-menu[data-cm-id='${cm_id}']`).closest(".comment-of");
            $('html, body').animate({scrollTop: (edit_div.offset().top-55)}, 500, function(){
                edit_div.css("background-color", "#07C044");
                edit_div.fadeOut(1000, 'linear', function(){
                    this.remove();
                    if(!($('.comment-of').length)){
                        $("#comments").html('<div class="comment-of no-comment dis-color">'+gettext('No Comment')+'</div>');
                    }
                });
                $("#chx0dmxd").html('');
            });
        });
        response.fail(function(xhr, status, error){
            hidePop();
            if(xhr.status==404){
                errorMessageHandler(guess=gettext("Comment might have been deleted already."));
            } else {
                errorMessageHandler(guess=gettext("Could not delete comment."));
            }
        });
    });
});

$("#comment-btn").on("click", function(){
    if($(this).attr("type") !== "submit"){
        var comment = comment_area.val();
        comment = comment.trim();
        var is_edit = $("#cancel-edit").hasClass("d-none") ? false : true;
        try{
            cm_id = $("#edit-cm").data("cm-id");
        } catch{
            cm_id = null;
        }
        if(comment.length !== 0){
            var data = {
                'comment': comment,
                'csrfmiddlewaretoken': csrf
            }
            if(commentEditOpen() && cm_id !== null){
                data['cm_id'] = cm_id;
            }
            var response = $.ajax({
                type: "POST",
                url: `${root_url}/add-comment/`,
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
                            $.get('added-comment/'+comment_id+'/', function(data){ 
                                edit_div.replaceWith(data);
                            });
                        });
                    } else {
                        socket.send(JSON.stringify({"desc": "comment_added", "cm_id": comment_id}));
                        manageTotalComments("+");

                        $.get(`${root_url}/added-comment/${comment_id}/`, function(data){ 
                            $("#comments").append(data);
                            if($(".comment-of").hasClass('no-comment')){
                                $($(".comment-of.no-comment")).remove();
                            }
                        });
                    }                    
                } 
                else if(result.status == 'MAX_COMMENT'){
                    disableNewComment();
                    errorMessageHandler(guess=gettext("Maximum comment reached on the post!!!"), sol=gettext("So, you cannot comment on this post."), extra="");
                }            
                else {
                    addCmmntMssgErrHandler(data.comment, cm_id);
                }
            });
            response.fail(function(xhr, status, error){
                addCmmntMssgErrHandler(data.comment, cm_id);
            });
        }
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
    $("#comment-btn").text(gettext("Comment"));
    comment_area.attr("placeholder", gettext("Add a comment.."));
    $("#chx0dmxd").html('');
    hideTextArea();
});
/** Load new comments */
$("#new-comments").on("click", function(){
    $(this).removeClass("new-comments-p").html("");
    $.get(`${root_url}/new-comments/${new_cmnt_count}/`, function (data, textStatus, jqXHR){
        new_cmnt_count = 0;
        $("#comments").append(data);
        
    }).fail(function(){
        errorMessageHandler(guess=gettext("Could not load new comments."), sol=gettext("Try again!!!"), extra='');
        showNewComment(new_cmnt_count);
    });
});



/* Show reply input box on reply click */
$("#comments").on("click", ".show-reply", function(){
    cm_id = $(this).attr("data-cm-id");
    html_of_reply = $(this).html();

    if(isReplyOpened()){
        $(".show-reply").html(gettext("Reply"));
    }
    if(html_of_reply == gettext("Reply")){
        $(this).closest("div").next(".replies-cont").append(reply_box);
        $("#reply-btn").attr('data-cm-id', cm_id);
        reply_box.css("display", "flex");
        reply_area.focus();
        $(this).html(gettext("Hide"));
    } else {
        reply_box.hide("fast");
        $(this).html(gettext("Reply"));
    }
});
reply_area.keyup(function(){
    if($(this).val().length >= 1){
        $("#reply-btn").removeAttr("disabled");
    } else {
        $("#reply-btn").attr("disabled", "");
    }

    if($(this).val().length >= 50){
        $(this).attr("rows", "3");
    } else {
        $(this).attr("rows", "1");
    }
});
/* Reply clicked */
$("#reply-btn").click(function(){
    if($(this).attr("type") !== "submit"){
        reply_btn = $(this);
        cm_id = $(this).attr("data-cm-id");
        var data = {
            'csrfmiddlewaretoken': csrf,
            'cm_id': cm_id,
            'reply': reply_area.val()
        }
        var response = $.ajax({
                        type: "POST",
                        url: `${root_url}/comment/${cm_id}/add-reply/`,
                        data: data
                    });
        $(this).attr("disabled", "disabled");
        response.done(function(result){
            rp_id = result.id;
            if(rp_id == 'MAX_REPLY'){
                errorMessageHandler(guess=gettext("Maximum reply reached on the comment!!!"), sol=gettext("So, you cannot reply on this comment."), extra="");
            }
            else {
                if(typeof cm_id === "undefined"){
                    cm_id=99;
                }
                socket.send(JSON.stringify({"desc": "reply_added", "cm_id": cm_id, "rp_id": rp_id}));
        
                $.get(`${root_url}/comment/${cm_id}/added-reply/${rp_id}/`, function(data){
                    var reply_div_of_new = reply_btn.parents("div.reply-inpt-box").prev("div.replies-in");
                    if(reply_div_of_new.html().trim().length == 0){
                        reply_div_of_new.html(data);
                    } else {
                        reply_div_of_new.children("div.reply-of").last().after(data);
                    }
                    reply_div_of_new.animate({scrollTop: reply_div_of_new.prop("scrollHeight")}, 500);
                });
            }
            reply_area.val("");
            reply_box.hide("fast");
            $(".show-reply").html(gettext("Reply"));
        });
        response.fail(function(xhr, status, error){
            reply_btn.removeAttr("disabled");
            errorMessageHandler(guess=gettext("Could not add reply."), sol=gettext("Try again!!!"), extra='');
        });
    }
});

/* View replies on click, New repliess */
$("#comments").on("click", ".more-replies", function(){
    var reply_p = $(this);
    var current_html = $(this).html();
    var data_cm_id = $(this).attr("data-cm-id").split("&_");
    var cm_id = parseInt(data_cm_id[0]); 
    if($(this).hasClass("showing")){
        reply_p.html(gettext('Show replies'));
        reply_p.next("div.replies-in").children("div.reply-of").slice(0, -2).hide();
        reply_p.removeClass("showing").addClass("shown");
    }
    else if($(this).hasClass("shown")) {
        reply_p.html(gettext('Hide replies'));
        reply_p.removeClass("shown").addClass("showing");
        reply_p.next("div.replies-in").children("div.reply-of").show();
    }
    else {
        var response = $.get(`${root_url}/comment/${cm_id}/view-replies/`);
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
            reply_p.html(current_html);
            errorMessageHandler(guess=gettext("Could not load new replies."), sol=gettext("Try again!!!"), extra='');
        });
    }
});

/**Delete replies */
$(document).on("click", ".rpl-del", function(e){
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
            url: `${root_url}/comment/${cm_id}/del-reply/${rp_id}/`,
            data: {
                'csrfmiddlewaretoken': csrf,
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
            if(xhr.status==404){
                errorMessageHandler(guess=gettext("Reply might have been deleted already."));
            } else {
                errorMessageHandler(guess=gettext("Could not delete reply."));
            }
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



/*
$("#more-comments").click(function(){
    $("#more-comments").css({"pointer-events": "none"});
    $("#comments").after("<span class='load-cic mg-t10'><span style='background-color: #999; height: 1.8rem; width: 1.8rem;'></span></span>");
    var req = $.ajax({
        url: `${root_url}/more-comment/`,
        type: 'POST',
        headers:{
            "X-CSRFToken": csrf
        },
        data: {
            "no": comment_loaded
        }
    });
    req.done(function(response){
        if(response.full_load){
            $("#more-comments").remove();
        } else {
            if($("#comments .comment-of:first-child").hasClass("dis-color")){
                $("#comments .comment-of:first-child").remove();
            }
            $("#comments").append(response);
            if($("#comments .comment-of:last-child").hasClass("d-none")){
                $("#more-comments").remove();
            } else {
                comment_loaded++;
                $("#more-comments span").html(parseInt($("#more-comments span").html())-MAX_POST_LOAD);
            }
        }
        $(".load-cic").remove();
    });
    req.fail(function(response){
        $(".load-cic").remove();
        errorMessageHandler(guess="Could not load comments.", sol=gettext("Try again!!!"), extra='');
    });
    req.always(function(response){
        $("#more-comments").css({"pointer-events": "auto"});
    });
}); */