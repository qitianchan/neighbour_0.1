/**
 * Created by Administrator on 2015/10/6.
 */

(function($){

    $(function(){

        // 地址
        var $pAddress = $("#pAddress").click(function(){
            G.PopList.addList(addressList,"code","address",setAddress).show();
        });

        var $ulPartner = $("#ulPartner").delegate(".del","click",function(){
            var $this = $(this),
                k = $this.closest("li").attr("key");
            //alert(k);
        });

        // test
        var addressList = [{code:"01",address:"凤凰小区阳光花园5-501"},{code:"02",address:"天骄豪庭1001号"}];
        var partnerList = [{code:"01",name:"胡太太",phone:"18822222222"},
            {code:"02",name:"胡莱",phone:"18822222222"},
            {code:"03",name:"胡图",phone:"18822222200"}];

        setAddress(addressList[0].code,addressList[0].address);
        loadPartnerList(partnerList);

        function loadPartnerList(partnerList){
            for(var i = 0,len = partnerList.length; i < len; i++){
                addPartner(partnerList[i]);
            }
        }

        function addPartner(partner){
            var $temp = $("#temp").children().clone();
            $temp.attr("key",partner.code);
            $("._name",$temp).text(partner.name);
            $("._phone",$temp).text(partner.phone.replace(/^(\d{3})(\d{5})(\d+)/,"$1*****$3"));
            $ulPartner.append($temp);
        }

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