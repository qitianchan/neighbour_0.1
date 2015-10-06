/**
 * Created by Administrator on 2015/10/6.
 */

(function($){

    $(function(){

        // 导航条
        var $ulNav = $("#ulNav").delegate("li","click",function(){
            var $this = $(this),
                k = $this.attr("key");
            if($this.hasClass("on")){
                return;
            }
            $ulNav.find(".on").removeClass("on");
            $this.addClass("on");

        });

        // 订单操作
        var $ulOrder = $("#ulOrder").delegate("._receipt","click",function(){
            var $this = $(this),
                k = $this.closest("li").attr("key");
            if(confirm("确认收货?")){

            }
        }).delegate("._evaluate","click",function(){
            var $this = $(this),
                k = $this.closest("li").attr("key");
            window.location.href = "evaluate.shtml?code="+k;
        });

        // test
        var orderList = [{url:"../images/rice.png",title:"稻花香五常大米，精选优质东北大米。5KG",count:"3",totalFee:"165",shipping:"0",status:"4",code:"01"},
            {url:"../images/rice.png",title:"稻花香五常大米，精选优质东北大米。5KG",count:"3",totalFee:"165",shipping:"0",status:"5",code:"02"},
            {url:"../images/rice.png",title:"稻花香五常大米，精选优质东北大米。5KG",count:"3",totalFee:"165",shipping:"0",status:"6",code:"03"}];

        loadOrderList(orderList);

        /**
         * 载入订单
         * @param orderList
         */
        function loadOrderList(orderList){
            for(var i = 0,len = orderList.length; i < len; i++){
                addOrder(orderList[i]);
            }
        }

        /**
         * 添加订单项
         * @param order
         */
        function addOrder(order){
            var $temp = $("#temp").children().clone();
            $temp.attr("key",order.code);
            $("._title",$temp).text(order.title);
            $("._pic",$temp).attr({src:order.url,alt:order.title});
            $("._detail",$temp).text("共"+order.count+"件 合计："+order.totalFee+"元（含运费"+order.shipping+"元）");
            if(order.status == ORDER_STATUS.DELIVERY){
                $("._status",$temp).text("待收货");
                $("._action",$temp).text("确认收货").addClass("btn-normal _receipt");
            }else if(order.status == ORDER_STATUS.RECEIPT){
                $("._status",$temp).text("待评价");
                $("._action",$temp).text("评价").addClass("btn-normal _evaluate");
            }else if(order.status == ORDER_STATUS.EVALUATED){
                $("._status",$temp).text("已评价");
                $("._action",$temp).text("已评价");
            }
            $ulOrder.append($temp);
        }

    });

})(jQuery);