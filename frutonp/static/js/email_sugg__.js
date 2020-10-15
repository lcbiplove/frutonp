$(document).ready(function(){
    function emailSugg(){
        $(".em-dom-sug").click(function(){
            var text = $("input[type=email]").val();
            if(text.length > 0){
                var index = text.indexOf("@");
                if(index== -1){
                    $("input[type=email]").val(text+$(this).html());
                } else {
                    $("input[type=email]").val(text.slice(0, index) + $(this).html());
                }
                $("input[type=email]").focus();
            } 
        });
    }
    $(document).click(function(e){
        if(e.target.className == "em-dom-sug" || e.target.type == "email"){
            $(".em-dom-sug").css("display", "inline");
            emailSugg();
        } else {
            $(".em-dom-sug").css("display", "none");
        }
    });
});