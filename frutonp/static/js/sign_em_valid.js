$(document).ready(function(){
    nameErr = true;
    emailErr = true;
    passErr = true;
    confPassErr = true;
    captchaErr = true;
    phoneErr = true;
    var tick = '<i class="far fa-check-circle"></i>';

    $("#validate-signup").trigger("reset");

    function uniqueErr() {
        if($(".of-email .err-mssg").children().length > 0){
            return true;
        } else {
            return false;
        }
    }

    function nameChk(par){        
        if(par.length > 4 && par.length < 49){
            if(/^[a-zA-Z-_ ]*$/.test(par)){
                $("#cor-of-name").html(tick);
                $(".of-name .err-mssg").html("");
                $('input[name=name]:focus').css({'box-shadow' : '#07C044 0px 0px 2px 2px'});
                return false;
            } else {
                $("#cor-of-name").html("");
                errMssg = "Should not contain other characters except letters, hyphens, underscore and spaces.";
                $(".of-name .err-mssg").html(errMssg);
                $('input[name=name]:focus').css({'box-shadow' : '#b00 0px 0px 2px 2px'});
                return true;
            }
            
        } else {
            $("#cor-of-name").html("");
            errMssg = "Must be more than 4 characters";
            $(".of-name .err-mssg").html(errMssg);
            $('input[name=name]:focus').css({'box-shadow' : '#b00 0px 0px 2px 2px'});
            return true;
        }
    }

    function phoneChk(par){        
        if(par.length == 10 && /^\d+$/.test(par)){
            $("#cor-of-phone").html(tick);
            $(".of-phone .err-mssg").html("");
            $('input[name=phone]:focus').css({'box-shadow' : '#07C044 0px 0px 2px 2px'});
            return false;
        } else {
            $("#cor-of-phone").html("");
            errMssg = "Phone number must be of 10 numbers";
            $(".of-phone .err-mssg").html(errMssg);
            $('input[name=phone]:focus').css({'box-shadow' : '#b00 0px 0px 2px 2px'});
            return true;
        }
    }

    function emailChk(par){
        if(/^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/.test(par)){
            $("#cor-of-email").html(tick);
            $(".of-email .err-mssg").html("");
            $('input[name=email]:focus').css({'box-shadow' : '#07C044 0px 0px 2px 2px'});
            return false;
        } else {
            $("#cor-of-email").html("");
            errMssg = "Invalid email pattern";
            $(".of-email .err-mssg").html(errMssg);
            $('input[name=email]:focus').css({'box-shadow' : '#b00 0px 0px 2px 2px'});
            return true;
        }
    }

    function passChk(par){
        if(/^(?=.*[a-z])(?=.*[0-9])(?=.{8,})/.test(par)){
            $(".of-pass .err-mssg").html("");
            $('input[name=pass]:focus').css({'box-shadow' : '#07C044 0px 0px 2px 2px'});
            return false;
        } else {
            errMssg = "Must be at least 8 characters with lowercase and number characters";
            $(".of-pass .err-mssg").html(errMssg);
            $('input[name=pass]:focus').css({'box-shadow' : '#b00 0px 0px 2px 2px'});
            return true;
        }
    }

    function confPassChk(par, pass){
        if(par == pass){
            $(".of-pass-conf .err-mssg").html("");
            $('input[name=confPass]:focus').css({'box-shadow' : '#07C044 0px 0px 2px 2px'});
            return false;
        } else {
            errMssg = "Password does not match";
            $(".of-pass-conf .err-mssg").html(errMssg);
            $('input[name=confPass]:focus').css({'box-shadow' : '#b00 0px 0px 2px 2px'});
            return true;
        }
    }
    
    function already_email(inp) {
        par = inp;
        csrfmiddlewaretoken = $('input[name=csrfmiddlewaretoken]').val();
        $.ajax({
            type: "POSt",
            url: "/join/aj_ch_em/",
            data: {
                csrfmiddlewaretoken: csrfmiddlewaretoken,
                em_ok_lkng_of: par
            },
            dataType: 'json'
        }).done(function(data){
            var already = (data['status'] === 'true');
            if(already){
                $("#cor-of-email").html("");
                errMssg = "The email already exists";
                $(".of-email .err-mssg").html(errMssg);
                $('input[name=email]:focus').css({'box-shadow' : '#b00 0px 0px 2px 2px'});
            } else {
                $("#cor-of-email").html(tick);
                $(".of-email .err-mssg").html("");
                $('input[name=email]:focus').css({'box-shadow' : '#07C044 0px 0px 2px 2px'});
                if(validate()){
                    $("#form-sub").removeAttr("disabled", "disabled");
                } else {
                    $("#form-sub").attr("disabled", "");
                }
            }
        });
    }

    function validate(){
        if(nameErr || emailErr || passErr || confPassErr || uniqueErr() || captchaErr || phoneErr){
            if(nameErr){
                nameChk($("input[name=name]").val());
            } 
            if(phoneErr){
                phoneChk($("input[name=phone]").val());
            }
            if(emailErr){
                emailChk($("input[name=email]").val());
            }
            if(passErr){
                passChk($("input[name=pass]").val());
            }
            if(confPassErr){
                confPassChk($("input[name=confPass]").val());
            }
            return false;
        } else {
            return true;
        }
    }

    function is_captcha(){
        var response = grecaptcha.getResponse();
        if(response.length == 0){
            return false;
        } else {
            return true;
        }
    }

    window.onReCaptchaSuccess = function(){
        captchaErr = false;
        if(validate()){
            $("#form-sub").removeAttr("disabled", "disabled");
        } else {
            $("#form-sub").attr("disabled");
        }
    }

    window.recaptchaExpired = function(){
        $("#form-sub").attr("disabled", "disabled");
    }

    $("input[name=name]").keyup(function(){
        nV = $(this).val();
        nameErr = nameChk(nV);       
    });

    $("input[name=phone]").keyup(function(){
        nV = $(this).val();
        phoneErr = phoneChk(nV);       
    });

    $("input[name=email]").keyup(function(){
        nV = $(this).val();
        emailErr = emailChk(nV);

        if(!emailErr){
            already_email(nV);
        }
    });

    $("input[name=pass]").keyup(function(){
        nV = $(this).val();

        passErr = passChk(nV);

        $("input[name=confPass]").keyup();
    });

    $("input[name=confPass]").keyup(function(){
        nV = $(this).val();

        confPassErr = confPassChk(nV, $("input[name=pass]").val());
    });        

    $(".em-dom-sug").click(function(){
        text = $(this).text();
        val = $("input[name=email]").val().split("@", 1);
        total = val+text;
        emailChk(total);
        if(!emailChk(total)){
            already_email(total);
            emailErr = false;
        } else {
            emailErr = true;
        }
    });

    $("form input").focus(function(){
        if($(this).attr("name") == "name"){
            if(nameErr){
                $('input[name=name]:focus').css({'box-shadow' : '#b00 0px 0px 2px 2px'});  
            }   else {
                $('input[name=name]:focus').css({'box-shadow' : '#07C044 0px 0px 2px 2px'});  
            }
        } 

        if($(this).attr("name") == "phone"){
            if(nameErr){
                $('input[name=phone]:focus').css({'box-shadow' : '#b00 0px 0px 2px 2px'});  
            }   else {
                $('input[name=phone]:focus').css({'box-shadow' : '#07C044 0px 0px 2px 2px'});  
            }
        } 
        
        if($(this).attr("name") == "email"){
            if(emailErr || uniqueErr()){
                $('input[name=email]:focus').css({'box-shadow' : '#b00 0px 0px 2px 2px'});  
            }   else {
                $('input[name=email]:focus').css({'box-shadow' : '#07C044 0px 0px 2px 2px'});  
            }
        } 

        if($(this).attr("name") == "pass"){
            if(passErr){
                $('input[name=pass]:focus').css({'box-shadow' : '#b00 0px 0px 2px 2px'});  
            } else {
                $('input[name=pass]:focus').css({'box-shadow' : '#07C044 0px 0px 2px 2px'});  
            }
        } 

        if($(this).attr("name") == "confPass"){
            if(confPassErr){
                $('input[name=confPass]:focus').css({'box-shadow' : '#b00 0px 0px 2px 2px'});  
                } else {
                $('input[name=confPass]:focus').css({'box-shadow' : '#07C044 0px 0px 2px 2px'});  
            }
        }
    });

    $(".sign-create-sub").click(function(){
        console.log(is_captcha());
    })

    $("input").keyup(function(){
        captchaErr = !is_captcha();
        if(validate()){
            $("#form-sub").removeAttr("disabled", "disabled");
        } else {
            $("#form-sub").attr("disabled", "");
        }
    });

    $("#validate-signup").submit(function(e) {
        if(!validate() && !uniqueErr() && !is_captcha()){
            e.preventDefault();
        } else {
            $(this).submit();
        }
    });
});