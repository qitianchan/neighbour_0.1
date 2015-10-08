/**
 * Created by Administrator on 2015/10/5.
 */
(function($){

    $(function(){

        var $ulRecords = $("#ulRecords").delegate("li","click",function(){
            var $this = $(this),
                k = $this.attr("key");
            window.location.href = "repairs.shtml?repairs_id="+k;
        });

        /*
        //test
        var recordList = [{fixOrderID:"01",content:"我家厕所堵了，麻烦帮我疏通一下",timeStr:"10-01 15:20",status:"0"},
            {fixOrderID:"02",content:"我家厕所堵了，麻烦帮我疏通一下",timeStr:"10-01 15:20",status:"1"},
            {fixOrderID:"03",content:"我家厕所堵了，麻烦帮我疏通一下",timeStr:"10-01 15:20",status:"2"}];
        loadRecordList(recordList);
        */

        Sandbox(["server"],function(box){

            box.getRepairOrders(function(d){
                loadRecordList(d.fixOrderList);
            });

        });

        /**
         * 载入记录列表
         * @param recordList
         */
        function loadRecordList(recordList){
            for(var i = 0,len = recordList.length; i < len; i++){
                addRepairRecord(recordList[i]);
            }
        }

        /**
         * 添加记录项
         * @param record
         */
        function addRepairRecord(record){
            var $temp = $("#temp").children().clone();
            $temp.attr("key",record.fixOrderID);
            $("._title",$temp).text(record.content);
            $("._time",$temp).text(record.timeStr);
            if(record.status == REPAIRS_STATUS.UNHANDLED){
                $("._status",$temp).text("催一下").addClass("push");
            }else if(record.status == REPAIRS_STATUS.ACTIVE){
                $("._status",$temp).text("处理中").addClass("active");
            }else if(record.status == REPAIRS_STATUS.FINISH){
                $("._status",$temp).text("已结束").addClass("over");
            }
            $ulRecords.append($temp);
        }
    });

})(jQuery);