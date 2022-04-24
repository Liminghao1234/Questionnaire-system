$(document).ready(function (){
    var hide = function () {
        $(".single").hide();
        $(".multiple").hide();
        $(".completion").hide();
    }
    hide();
    $("#inputState").change(function (){
        var type = $(":selected").val();
        switch (type){
            case "single choice":
                hide();
                $(".single").show();
                break;
            case "multiple choice":
                hide();
                $(".multiple").show();
                break;
            case "completion":
                hide();
                $(".completion").show();
                break;
            case "default":
                hide();
                break;
        }
    });
    var i = 2;
    $(".add-single").click(function (){
        var input = "<input type=\"text\" name=\"single"+i+"\" class=\"form-control single-inout\" placeholder=\"option"+i+"\" >";
        $(".single-input").append(input);
        i++;
    });
    var j = 2;
    $(".add-multiple").click(function (){
        var input = "<input type=\"text\" name=\"multiple"+j+"\" class=\"form-control multiple-inout\" placeholder=\"option"+j+"\" >";
        $(".multiple-input").append(input);
        j++;
    });

});