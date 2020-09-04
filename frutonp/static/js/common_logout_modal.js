$(document).ready(function(){
    $("#logout").on('click', function(){
        $("#logout-form").submit();
    });
    try{
        classFromClose = $(".modal-close").attr("class").split('')[1]; // To get the class name of which modal
    }
    catch {
        classFromClose = "";
    }
    $(".modal-close").on('click', function(){
        var modalId = "#"+classFromClose+"-modal";
        $(".modal-close").css("display", "none");
        window.history.go(-1);
    });
});