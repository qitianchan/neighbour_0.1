/**
 * Created by Administrator on 2015/10/6.
 */

(function($){

    $(function(){

        var $spStars = $("#spStars").delegate("span","click",function(){
            var $this = $(this),
                k = $this.attr("key");
            $spStars.attr("class","stars stars-"+k);
        });

        var $spTip = $("#spTip");

        var $taContent = $("#taContent").on("keyup",function(){
            var count = $taContent.val().length;
            $spTip.text(count+"/200");
        });
    });

})(jQuery);