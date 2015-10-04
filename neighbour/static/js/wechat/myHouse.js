/**
 * Created by Administrator on 2015/10/1.
 */
(function($){

    $(function(){

        var $ulHouse = $("#ulHouse"),
            $tempHouse = $("#tempHouse");

        // test
        var houseList = [{code:"01",address:"风享花园一期丰庭南街15号405",type:"0",phone:"18888888888"},
            {code:"02",address:"风享花园一期丰庭南街15号406",type:"1",phone:"1880000000"}];

        loadData(houseList);

        function loadData(houseList){
            var $temp,item;
            for(var i = 0,len = houseList.length; i < len; i++){
                item = houseList[i];
                $temp = $tempHouse.children().clone();
                //$temp.attr("key",item.code);
                $("._address",$temp).text(item.address);
                $("._role",$temp).text(ROLE_TYPE[item.type]);
                $("._phone",$temp).text(item.phone);
                //$(".edit",$temp).attr("href","/wechat/verify/submitForm.shtml?type=edit&code="+item.code);
                $(".delete",$temp).attr("key",item.code);
                $ulHouse.append($temp);
            }
        }
    });

})(jQuery);