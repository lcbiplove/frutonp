$(document).ready(function(){
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
});