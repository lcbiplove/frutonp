$(document).ready(function(){
    $(".in-sess-mssg").first().css({"bottom": "0px"});
    setTimeout(function(){
        $(".in-sess-mssg").last().css({"bottom": "0px"});
    }, 500);
    setTimeout(function(){
        $(".sess-success").css({"bottom": "-500px"});
    }, 10000);
    setTimeout(function(){
        $(".sess-info").css({"bottom": "-500px"});
    }, 20000);
    setTimeout(function(){
        $(".sess-error").css({"bottom": "-500px"});
    }, 30000);        
    
    $(".sess-close").on('click', function(){
        $(this).closest(".in-sess-mssg").css({"bottom": "-500px"});
    });
    $(".act-close").on('click', function(){
        $(".act-div").css({"bottom": "-1000px"});
    });
    $(".act-extra").on('click', function(){
        if($(this).html()=="Reload"){
            window.location.reload();
        }
    });
});
