/**
 * Created by Administrator on 2015/10/3.
 */

(function($){

    $(function(){

        // 地址
        var $pAddress = $("#pAddress").click(function(){
            G.PopList.addList(addressList,"code","address",setAddress).show();
        });

        // 收费项列表
        var $ulList = $("#ulList").delegate("li","click",function(){
            var $this = $(this);
            if($this.hasClass("unknown")){
                return;
            }
            $("._detail",$this).toggle();
            $("._show",$this).toggleClass("icon-up icon-detail");
        });

        // 月份显示
        var $divDate = $("#divDate").click(function(){
            $("#divSelectMonth").show();
        });

        // 月份选择框
        var $divMonthList = $("#divMonthList").delegate(".box","click",function(){
            var $this = $(this),
                k = $this.attr("key");
            dateIndex = k;
            setDate();
            $("#divSelectMonth").hide();
        });

        // 上个月份
        var $divPrevMonth = $("#divPrevMonth").click(function(){
            var $this = $(this);
            if(!$this.hasClass("on")){
                return;
            }
            dateIndex++;
            setDate();
        });

        // 下个月
        var $divNextMonth = $("#divNextMonth").click(function(){
            var $this = $(this);
            if(!$this.hasClass("on")){
                return;
            }
            dateIndex--;
            setDate();
        });

        // test
        var addressList = [{code:"01",address:"凤凰小区阳光花园5-501"},{code:"02",address:"天骄豪庭1001号"}];
        var billList = [{code:"01",name:"水费",fee:"15.9",status:"1",detailList:["本月读数：417","上个月读数：395","实际用量：22","单价：2.620","金额：57.64","基本水费：1.460*22=32.120","污水处理费：0.920*22=20.240","水资源、水利、公用事业费：5.28"]},
            {code:"02",name:"电费",fee:"156",status:"0",detailList:["本月读数：417","上个月读数：395","实际用量：22","单价：2.620","金额：57.64","基本水费：1.460*22=32.120","污水处理费：0.920*22=20.240","水资源、水利、公用事业费：5.28"]}];


        setAddress(addressList[0].code,addressList[0].address);
        loadFeeData(billList);

        var currentDate = "201501",dateList = [],dateIndex = 0,TOTAL = 12;
        dateList = createDateList(currentDate);
        loadDateList(dateList);
        setDate();

        /**
         * 设置地址信息
         * @param k
         * @param v
         */
        function setAddress(k,v){
            $pAddress.attr("key",k).text(v);
        }

        /**
         * 加载费用列表
         * @param billList
         */
        function loadFeeData(billList){
            for(var i = 0,len = billList.length; i < len; i++){
                addFeeItem(billList[i]);
            }
        }

        /**
         * 添加费用项
         * @param item
         */
        function addFeeItem(item){
            var $temp = $("#temp").children().clone();
            $temp.attr("key",item.code);
            $("._name",$temp).text(item.name);

            if(item.status == FEE_STATUS.UNKNOWN){
                $temp.addClass("unknown");
                $("._money",$temp).text("未出");
            }else if(item.status == FEE_STATUS.PAID){
                $temp.addClass("paid");
                $("._money",$temp).text(item.fee);
            }else if(item.status == FEE_STATUS.UNPAID){
                $temp.addClass("unpaid");
                $("._money",$temp).text(item.fee);
            }
            for(var i = 0,len = item.detailList.length; i < len; i++){
                $("._detail",$temp).append("<span>"+item.detailList[i]+"</span>");
            }
            $ulList.append($temp);
        }

        /**
         * 创建可选日期列表
         * @param dateStr
         * @returns {Array}
         */
        function createDateList(dateStr){
            var y = parseInt(dateStr.substr(0,4)),
                m = parseInt(dateStr.substr(4,2)),
                list = [];
            for(var i = 0; i < TOTAL; i++){
                list.push({y:""+y,m:(m < 10 ? "0"+m:""+m)});
                m--;
                if(m == 0){
                    m = 12;
                    y--;
                }
            }
            return list;
        }

        /**
         * 加载日期列表
         * @param dateList
         */
        function loadDateList(dateList){
            var d ;
            for(var i = 0,len = dateList.length; i < len; i++){
                d = dateList[i];
                addDateOption(d.y, d.m,i);
            }
        }

        /**
         * 构造可选日期项
         * @param y
         * @param m
         * @param k
         */
        function addDateOption(y,m,k){
            var htmlStr = "<div class='box' key='"+k+"'>"+m+"月<br/>"+y+"</div>";
            $divMonthList.append(htmlStr);
        }

        /**
         * 设置当前日期
         */
        function setDate(){
            var d = dateList[dateIndex];
            $(".year",$divDate).text(d.y);
            $(".month",$divDate).text(d.m+"月份");
            if(dateIndex == TOTAL-1){
                $divPrevMonth.removeClass("on");
            }else{
                $divPrevMonth.addClass("on");
            }
            if(dateIndex == 0){
                $divNextMonth.removeClass("on");
            }else{
                $divNextMonth.addClass("on");
            }
        }
    });

})(jQuery);