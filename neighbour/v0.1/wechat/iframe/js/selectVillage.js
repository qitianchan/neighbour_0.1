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
                loadVillage(allVillage);
            }else{
                var area = G.findByAttr(allAreaList,"area_id",k);
                loadVillage(area.villageList);
            }
        });

        //$divVillage.delegate("li","click",function(){
        //    var $this = $(this),
        //        k = $this.attr("key");
        //    window.location.href = "submitForm.shtml?village_id="+k;
        //});

        // test
        var allAreaList = [{area_id:"01",area_name:"天河",villageList:[
            {village_id:"01001",village_name:"华景新城"},
            {village_id:"01002",village_name:"都市华庭"},
            {village_id:"01003",village_name:"中怡城市花园"},
            {village_id:"01004",village_name:"祥龙花园"}
        ]},
            {area_id:"02",area_name:"越秀",villageList:[{village_id:"02001",village_name:"越秀01"}]},
            {area_id:"03",area_name:"番禺",villageList:[]},
            {area_id:"04",area_name:"海珠",villageList:[]},
            {area_id:"05",area_name:"荔湾",villageList:[]},
            {area_id:"06",area_name:"花都",villageList:[]}],
            allVillage = [];

        loadData(allAreaList);

        function loadData(areaList){
            var htmlStr = "<li key='0'>全部</li>",area = null, i,len;
            for(i = 0,len = areaList.length; i < len; i++){
                area = areaList[i];
                htmlStr += "<li key='"+area.area_id+"'>"+area.area_name+"</li>";
                if(area.villageList.length > 0){
                    allVillage = allVillage.concat(area.villageList);
                }
            }
            $divArea.html(htmlStr);
            loadVillage(allVillage);
        }

        function loadVillage(villageList){
            var i,len,village,htmlStr = "";
            for(i=0,len = villageList.length; i < len; i++){
                village = villageList[i];
                htmlStr += "<li key='"+village.village_id+"'>"+village.village_name+"</li>";
            }
            $divVillage.html(htmlStr);
        }
    });

})(jQuery);