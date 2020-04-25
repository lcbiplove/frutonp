$(document).ready(function(){

    function emailSugg(){
        $(".em-dom-sug").css("display", "inline");
        $("input[type=email]").keyup(function(){
            text = $(this).val();
            value = [];
            for(i=0; i<text.length; i++){
                if(text[i] == "@"){
                    break;
                }
                value += text[i];
            }
            domain = "";
            $(".em-dom-sug").click(function(){
                if(text.length > 0){
                    domain = $(this).text();
                    final = value + domain;
                    $("input[type=email]").val(final);
                    $("input[type=email]").focus();
                } 
            });
        });
    }

    $(document).click(function(e){
        if(e.target.className == "em-dom-sug" || e.target.type == "email"){
            emailSugg();
        } else {
            $(".em-dom-sug").css("display", "none");
        }
    });

});