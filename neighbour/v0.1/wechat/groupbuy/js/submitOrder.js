/**
 * Created by Administrator on 2015/10/6.
 */

(function($){

    $(function(){

        var $tbNum = $("#tbNum");
        var $btnMinus = $("#btnMinus").click(function(){
            var v = parseInt($tbNum.val());
            if(!isNaN(v) && v > 0){
                $tbNum.val(v-1);
            }
        });
        var $btnPlus = $("#btnPlus").click(function(){
            var v = parseInt($tbNum.val());
            if(!isNaN(v)){
                $tbNum.val(v+1);
            }
        });

    });

})(jQuery);