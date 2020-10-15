$(document).ready(function(){
    const MAX_POST_LOAD = 20;
    var showPop = Pop.showPop;
    var hidePop = Pop.hidePop;
    var popShown = Pop.popShown;
    var csrf = $("[name=csrfmiddlewaretoken]").val();
    var wait_scroll = false;
    var post_loaded = 1;
    
    function getIdOfClass(param){
        return $(param).attr("id");
    }
    /* Posts, myaccounts tab */
    $(".prfl-box-ttl").on("click", function(){
        var id = getIdOfClass(this);
        var contOfId = "#" + id + "-content";
        
        $(".prfl-box-content").css({"display":"none"});
        $(contOfId).css({"display": "block"});
        $(".prfl-box-ttl").removeClass("prfl-active");
        $(this).addClass("prfl-active");
    });

    $("#upload-pp-anc").click(function(e){
        e.preventDefault();
        e.stopPropagation();
        $("#pp-upload").trigger("click");
    });
    $("#pp-upload").click(function(){
        var rmv_btn = "";
        var is_default_pp = $(this).attr("data-def-pp") == 'true';
        if(!is_default_pp){
            rmv_btn = "<div><button style='color: rgb(245, 51, 51); background-color: #f0f0f0;' id='upload-rm-pp'>"+gettext('Remove Photo')+"</button></div>";
        }
        $("#chx0dmxd").html("<div class='real-modal'><div class='real-modal-container' tabindex='0'><div class='real-modal-header'><div>Profile Picture</div><div class='real-modal-close'>&times;</div></div><div class='real-modal-body text-center'><div><button id='upload-pp-main'>"+gettext("Upload Photo")+"</button></div>"+rmv_btn+"<div><button class='real-modal-close rm-rl-cl-dwn'>"+gettext('close')+"</button></div></div></div></div>");
        showPop();
    });
    $("#chx0dmxd").on("click", ".real-modal-close", function(){
        hidePop();
    });
    $("#chx0dmxd").on("click", "#upload-pp-main", function(){
        $("#upload-pp").trigger('click');
    });

    $(document).on("click", function(e){
        if(e.target.id !== "pp-upload")
            if($(e.target).parents(".real-modal-container").length == 0)
                if(popShown)
                    hidePop(); 
    });
    // On image is selected
    $("#upload-pp").change(function(){
        // if selected image is not null
        if($(this).val().length > 0)
            $("#pp-form").attr("action", "upload-pp/").each(function(){
                $(this).submit();
            });
    });
    // Delete pp
    $("#chx0dmxd").on("click", "#upload-rm-pp", function(){
        $("#pp-form-2").attr("action", "delete-pp/").each(function(){
            $(this).submit();
        });
    });
    if(!$("#post-content ol li").hasClass("dis-color") && $("#post-content ol li").length >= MAX_POST_LOAD){
        $(window).scroll(function() {
            if(((window.innerHeight + window.scrollY) >= document.body.offsetHeight) && !wait_scroll) {
                wait_scroll = true;
                $("#post-content ol").append('<li class="fl-mid loading-more-post"><span class="my-small-load"><span></span></span></li>');
                var req = $.ajax({
                    url: 'profile-post/',
                    type: 'POST',
                    headers:{
                        "X-CSRFToken": csrf
                    },
                    data: {
                        "no": post_loaded
                    }
                });
                req.done(function(response){
                    $(".loading-more-post").remove();
                    if(response.full_load){
                        wait_scroll = true;
                    } else {
                        if($("#post-content ol li:first-child").hasClass("dis-color")){
                            $("#post-content ol li:first-child").remove();
                        }
                        $("#post-content ol").append(response);
                        if($("#post-content ol li:last-child").hasClass("d-none")){
                            wait_scroll = true;
                        } else {
                            wait_scroll = false;
                            post_loaded++;
                        }
                    }
                });
            }
        });
    }
    $(".post-del").on("click", function(e){
        e.preventDefault();
        var post_id = $(this).attr("data-pid");
        $("#chx0dmxd").html('<div class="real-modal"><div class="real-modal-container" tabindex="0"><div class="real-modal-header" style="background-color: #ff4a4a;"><div>'+gettext('Delete')+'</div><div class="real-modal-close">&times;</div></div><div class="real-modal-body" style="padding: 10px 10px 10px 20px;">'+gettext('Are you sure you want to delete the post?')+'</div><div class="modal-del-options"><button id="del-yes">'+gettext('Yes')+'</button><button class="real-modal-close" id="del-no">'+gettext('No')+'</button></div></div></div>');
        showPop();
        e.stopPropagation();
        $("#del-yes").on("click", function(e){  
            $(".real-modal-container").addClass("back-trans fl-mid").html(Pop.load_elips);
            e.stopPropagation();
            var response = $.ajax({
                type: "POST",
                url: `/post/delete/`,
                data: {
                    'csrfmiddlewaretoken': csrf,
                    'pid': post_id
                },
                cache: false
            });
            response.done(function(result){
                hidePop();
                if(result.status){
                    $(`a[data-pid=${post_id}]`).closest("li").animate({"opacity": "0"}, 1000, function(){
                        $("#post span").html(parseInt($("#post span").html())-1);
                        $(`a[data-pid=${post_id}]`).closest("li").remove();
                        if(!$("#post-content ol").children().length){
                            $("#post-content ol").html('<li class="dis-color">'+gettext('No post')+'</li>')
                        }
                    });
                    $("#chx0dmxd").html('');
                } 
            });
            response.fail(function(xhr, status, error){
                hidePop();
                if(xhr.status==404){
                    $(".act-guess").html(gettext("Post might have been deleted already."));
                } else {
                    $(".act-guess").html(gettext("Could not delete post."));
                }
                $(".act-sol").html(gettext("Try again or reload the page."));
                $(".act-extra").html(gettext("Reload"));
                $(".act-div").css({"bottom": "0px"});
                setTimeout(function(){
                    $(".act-div").css({"bottom": "-1000px"});
                }, 20000); 
            });
        });
    });
});