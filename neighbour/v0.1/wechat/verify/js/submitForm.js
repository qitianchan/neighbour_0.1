/**
 * Created by Administrator on 2015/10/1.
 */
(function($){

    $(function(){

        var $pSelectVillage = $("#pSelectVillage"),
            $divSelectVillage = $("#divSelectVillage"),
            $divVillage = $("#divVillage"),
            $pVillage = $("#pVillage"),
            $spProject = $("#spProject"),
            $spBuilding = $("#spBuilding"),
            $spRoom = $("#spRoom"),
            $spRole = $("#spRole"),
            $btnSendCode = $("#btnSendCode");

        var cellList = [],buildingList = [],houseList = [],box;

        var paramObj = G.getQueryStrObj();

        if(paramObj.type == "edit"){

        }else{
            $divSelectVillage.show();
        }

        // 地址栏
        $pSelectVillage.click(function(){
            $divSelectVillage.show();
        });

        // 项目
        $("#divProject").click(function(){
            G.PopList.addList(cellList,"cellID","cellName",function(k,v){
                $spProject.attr("key",k).text(v);
                var cell = G.findByAttr(cellList,"cellID",k);
                if(cell != null){
                    buildingList = cell.buildingList;
                }
            }).show();
        });

        // 楼宇
        $("#divBuilding").click(function(){
            G.PopList.addList(buildingList,"buildingID","buildingName",function(k,v){
                $spBuilding.attr("key",k).text(v);
                var building = G.findByAttr(buildingList,"buildingID",k);
                if(building != null){
                    houseList = building.houseList;
                }
            }).show();
        });

        // 楼宇
        $("#divRoom").click(function(){
            G.PopList.addList(houseList,"houseID","houseCode",function(k,v){
                $spRoom.attr("key",k).text(v);
            }).show();
        });


        // 角色
        $("#divRole").click(function(){
            G.PopList.addList(ROLE_TYPE,function(k,v){
                $spRole.attr("key",k).text(v);
            }).show();
        });

        // 验证码发送按钮
        $btnSendCode.click(function(){
            $("#pTip").show();
        });

        // 提交按钮
        var $btnSubmit = $("#btnSubmit").click(function(){

        });

        Sandbox(["user"],function(box){
            // 地区选择
            $divVillage.delegate("li","click",function(){
                var $this = $(this),
                    k = $this.attr("key"),
                    v = $this.text();
                $pVillage.text(v).attr("key",k);
                resetForm();
                $divSelectVillage.hide();
                // 载入地区下的小区信息
                box.getAreaByCode(k,function(d){
                    cellList = d.cellList;
                });
            });

        });

        function resetForm(){
            $spProject.text("").attr("key","");
            $spBuilding.text("").attr("key","");
            $spRoom.text("").attr("key","");
            $spRole.text("").attr("key","");
        }
    });

})(jQuery);