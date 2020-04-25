$(document).ready(function(){

    $("#sess-mssg-div div").first().animate({"left": "10px"}, 700, function(){
        $("#sess-mssg-div div").last().animate({"left": "10px"}, 700);
    });
    
    $(".sess-close").on('click', function(){
        var parent = $(this).parent().get(0).className;
        var mainParent = parent.split(' ');
        $("."+mainParent).css({"left": "-400px", "transition": "left 0.7s"});
    });
});