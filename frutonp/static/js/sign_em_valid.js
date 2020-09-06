$(document).ready(function(){
    var nameErr = true;
    var emailErr = true;
    var passErr = true;
    var confPassErr = true;
    var captchaErr = true;
    var phoneErr = true;
    var tick_mark = '<i class="fas fa-check"></i>';
    var small_loader = '<i class="fa fa-spinner small-loader"></i>';
    var namePattern = /^[A-Za-z]+([-_ ][A-Za-z]+)*$/;
    var emailPattern = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/;
    var passPattern = /^(?=.*[a-z])(?=.*[0-9])(?=.{8,})/;
    var phonePattern = /^\d+$/;
    $("#validate-signup").trigger("reset");
    window.onReCaptchaSuccess = function(){
        captchaErr = false;
        if(exceptCaptchaAllFine()){
            $("#form-sub").removeAttr("disabled");
        } else {
            $("#form-sub").attr("disabled", "disabled");
        }
    }
    window.recaptchaExpired = function(){
        captchaErr = true;
        $("#form-sub").attr("disabled", "disabled");
    }
    function already_email(email_){
        var request = $.ajax({
            url: '/join/aj_ch_em/',
            method: 'post',
            data: {
                "em_ok_lkng_of": email_,
            },
            headers:{
                "X-CSRFToken": $("input[name=csrfmiddlewaretoken]").val()
            }
        });
        request.done(function(response){
            if(response.status=="true"){
                $("#emailId").css({"box-shadow": "#c00 0px 0px 5px"});
                $("#cor-of-email").html("");
                $(".of-email .err-mssg").html("Email already exists");
                emailErr=true;
                $("#form-sub").attr("disabled", "disabled");
            } else {
                $("#cor-of-email").html(tick_mark);
                emailErr=false;
            }
        });
    }
    function nameChk(par){       
        if(par.length > 4 && par.length < 48){
            if(namePattern.test(par)){
                $("#nameId").css({"box-shadow": "#0c0 0px 0px 5px"});
                $("#cor-of-name").html(tick_mark);
                $(".of-name .err-mssg").html("");
                nameErr=false;
            } else {
                $("#nameId").css({"box-shadow": "#c00 0px 0px 5px"});
                $("#cor-of-name").html("");
                $(".of-name .err-mssg").html("Name may contain underscore, spaces or hypen only");
                nameErr=true;
            }
        } else {
            $("#nameId").css({"box-shadow": "#c00 0px 0px 5px"});
            $("#cor-of-name").html("");
            $(".of-name .err-mssg").html("Name should contain more than 4 and less than 48 characters");
            nameErr=true;
        }
    }
    function phoneChk(par){        
        if(par.length == 10 && phonePattern.test(par)){
            $("#phoneId").css({"box-shadow": "#0c0 0px 0px 5px"});
            $("#cor-of-phone").html(tick_mark);
            $(".of-phone .err-mssg").html("");
            phoneErr=false;
        } else {
            $("#phoneId").css({"box-shadow": "#c00 0px 0px 5px"});
            $("#cor-of-phone").html("");
            $(".of-phone .err-mssg").html("Phone should be 10 digit numbers");
            phoneErr=true;
        }
    }
    function emailChk(par){
        if(emailPattern.test(par)){
            $("#emailId").css({"box-shadow": "#0c0 0px 0px 5px"});
            //$("#cor-of-email").html(tick_mark);
            $("#cor-of-email").html(small_loader);

            $(".of-email .err-mssg").html("");
            emailErr=false;
            already_email(par);
        } else {
            $("#emailId").css({"box-shadow": "#c00 0px 0px 5px"});
            $("#cor-of-email").html("");
            $(".of-email .err-mssg").html("Email pattern does not match");
            emailErr=true;
        }
    }
    function passChk(par){
        if(passPattern.test(par)){
            $("#passId").css({"box-shadow": "#0c0 0px 0px 5px"});
            $(".of-pass .err-mssg").html("");
            passErr=false;
            if(par == $("#confPassId").val()){
                $("#confPassId").css({"box-shadow": "#0c0 0px 0px 5px"});
                $(".of-pass-conf .err-mssg").html("");
                confPassErr=false;
            } else {
                $("#confPassId").css({"box-shadow": "#c00 0px 0px 5px"});
                $(".of-pass-conf .err-mssg").html("Password does not match");
                confPassErr=true;
            }
        } else {
            $("#passId").css({"box-shadow": "#c00 0px 0px 5px"});
            $(".of-pass .err-mssg").html("Password should contain at least 8 characters with numbers, capital letters");
            passErr=true;
            if(par != $("#confPassId").val()) {
                $("#confPassId").css({"box-shadow": "#c00 0px 0px 5px"});
                $(".of-pass-conf .err-mssg").html("Password does not match");
                confPassErr=true;
            }
        }
    }
    function confPassChk(par){
        if(par == $("#passId").val()){
            if(passPattern.test(par)){
                $("#confPassId").css({"box-shadow": "#0c0 0px 0px 5px"});
            }
            $(".of-pass-conf .err-mssg").html("");
            confPassErr=false;
        } else {
            $("#confPassId").css({"box-shadow": "#c00 0px 0px 5px"});
            $(".of-pass-conf .err-mssg").html("Password does not match");
            confPassErr=true;
        }
    }
    function exceptCaptchaAllFine(){
        if(!emailErr && !nameErr && !phoneErr && !passErr && !confPassErr && !captchaErr) {
            $("#form-sub").removeAttr("disabled");
            return true;
        } else {
            $("#form-sub").attr("disabled", "disabled");
            return false;
        }
    }
    function validate(that){
        var inpt_id = that.id;
        switch (inpt_id) {
            case "nameId":
                nameChk(that.value);
                break;
            case "emailId":
                emailChk(that.value);
                break;
            case "phoneId":
                phoneChk(that.value);
                break;
            case "passId":
                passChk(that.value);
                break;
            case "confPassId":
                confPassChk(that.value);
                break;
            case "":
                var index = $("#emailId").val().indexOf("@");
                var par = index == -1 ? $("#emailId").val()+$(that).html() : $("#emailId").val().slice(0, index) + $(that).html();
                emailChk(par);
                break;
            default:
                break;
        }
        exceptCaptchaAllFine();
    }

    $("#validate-signup input").on("keyup", function(){
        validate(this);
    });
    $(".em-dom-sug").on("click", function(){
        validate(this);
    });
});