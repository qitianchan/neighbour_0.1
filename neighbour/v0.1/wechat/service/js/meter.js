/**
 * Created by Administrator on 2015/10/3.
 */

(function($){

    $(function(){

        var $pAddress = $("#pAddress").click(function(){
            G.PopList.addList(addressList,"code","address",setAddress).show();
        });

        var $pNav = $("#pNav").delegate("span","click",function(){
            var $this = $(this),
                k = $this.attr("key");
            $pNav.find(".on").removeClass("on");
            $this.addClass("on");
            $tbNum.val("");
        });

        var $tbNum = $("#tbNum");

        var $btnSubmit = $("#btnSubmit").click(function(){

        });


        // test
        var addressList = [{code:"01",address:"凤凰小区阳光花园5-501"},{code:"02",address:"天骄豪庭1001号"}];
        setAddress(addressList[0].code,addressList[0].address);

        Sandbox(["server"],function(box){
            box.getUploadBillStatus(function(d){
                console.log(d);
            });
        });

        function setAddress(k,v){
            $pAddress.attr("key",k).text(v);
        }
    });

})(jQuery);