/**
 * Created by Administrator on 2015/10/1.
 */
(function($){

    $(function(){
        // 自适应高度
        var h = $(document).height();
        var $divArea = $("#divArea"),
            $divVillage = $("#divVillage");
        $divArea.height(h-31);

        $divArea.delegate("li","click",function(){
            var $this = $(this),k;
            k = $this.attr("key");
            if(k == "0"){
                loadArea(allAreaList);
            }else{
                var area = G.findByAttr(allZoneList,"zoneID",k);
                loadArea(area.areaList);
            }
        });

        var allZoneList = [],allAreaList = [];

        Sandbox(["user"],function(box){
            box.getAreas(function(d){
                allZoneList = d.zoneList;
                loadData(allZoneList);
            });
        });

        // test
        /*
         var allAreaList = [{zoneID:"01",zoneName:"天河",areaList:[
         {areaID:"01001",areaName:"华景新城"},
         {areaID:"01002",areaName:"都市华庭"},
         {areaID:"01003",areaName:"中怡城市花园"},
         {areaID:"01004",areaName:"祥龙花园"}
         ]},
         {zoneID:"02",zoneName:"越秀",areaList:[{areaID:"02001",areaName:"越秀01"}]},
         {zoneID:"03",zoneName:"番禺",areaList:[]},
         {zoneID:"04",zoneName:"海珠",areaList:[]},
         {zoneID:"05",zoneName:"荔湾",areaList:[]},
         {zoneID:"06",zoneName:"花都",areaList:[]}],
         allVillage = [];
         loadData(allAreaList);
         */

        function loadData(zoneList){
            var htmlStr = "<li key='0'>全部</li>",zone = null, i,len;
            for(i = 0,len = zoneList.length; i < len; i++){
                zone = zoneList[i];
                htmlStr += "<li key='"+zone.zoneID+"'>"+zone.zoneName+"</li>";
                if(zone.areaList.length > 0){
                    allAreaList = allAreaList.concat(zone.areaList);
                }
            }
            $divArea.html(htmlStr);
            loadArea(allAreaList);
        }

        function loadArea(areaList){
            var i,len,area,htmlStr = "";
            for(i=0,len = areaList.length; i < len; i++){
                area = areaList[i];
                htmlStr += "<li key='"+area.areaID+"'>"+area.areaName+"</li>";
            }
            $divVillage.html(htmlStr);
        }
    });

})(jQuery);