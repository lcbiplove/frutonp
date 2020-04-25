$(document).ready(function(){


    $(".cookie-accept").on("click", function(){
        $(".cookie-alert-all").css({"visibility": "hidden", "transition": "opacity 2s"});
        $.ajax({
            url: "/__ck__law__",
            method: "GET"
        });
    });
    
});