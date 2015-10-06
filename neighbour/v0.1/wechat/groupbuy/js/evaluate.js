/**
 * Created by Administrator on 2015/10/6.
 */

(function($){

    $(function(){

        var $spTip = $("#spTip");

        var $taContent = $("#taContent").on("keyup",function(){
            var count = $taContent.val().length;
            $spTip.text(count+"/200");
        });
    });

})(jQuery);