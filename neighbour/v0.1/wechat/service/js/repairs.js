/**
 * Created by Administrator on 2015/10/5.
 */

(function($){

    $(function(){

        // test
        var addressList = [{code:"01",address:"凤凰小区阳光花园5-501"},{code:"02",address:"天骄豪庭1001号"}];


        // 地址
        var $pAddress = $("#pAddress").click(function(){
            G.PopList.addList(addressList,"code","address",setAddress).show();
        });

        var $btnSubmit = $("#btnSubmit");

        var paramObj = G.getQueryStrObj();
        if(paramObj["repairs_id"]){
            $("#div4Modify").show();
            $btnSubmit.hide();
        }else{
            $("#div4Modify").hide();
            $btnSubmit.show();
        }

        setAddress(addressList[0].code,addressList[0].address);

        /**
         * 设置地址信息
         * @param k
         * @param v
         */
        function setAddress(k,v){
            $pAddress.attr("key",k).text(v);
        }
    });

})(jQuery);